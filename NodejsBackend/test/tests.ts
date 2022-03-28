import { app } from "../src/index";
import chai from "chai";
import { expect } from "chai"
import chaiHttp from "chai-http";
import { createRequestObj } from '../src/util/scraper/createRequestObj'
import { ScraperRequest } from "../src/types/scraper/ScraperRequest";
import { pool } from "./poolClient"

chai.should();
chai.use(chaiHttp);

describe("Unit Tests", () => {
  
  describe("Test createRequestObj util function", () => {

    it("Given a list of urls it should return a ScraperRequest object", (done) => {
      const sampleUrls: string[] = [
        'https://www.theglobeandmail.com/canada/article-ukrainian-children-with-cancer-to-be-flown-to-toronto-hospital-for/',
        'https://www.businessinsider.com/private-jets-go-russia-dubai-after-putin-pledges-self-cleansing-2022-3',
        'https://www.businessinsider.com/russian-oligarch-helicopter-yacht-jets-ambramovich-isle-of-man-register-2022-3',
        'https://markets.businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3',
        'https://www.markets.businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3',
        'https://businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3'
      ]

      const scraperRequest: ScraperRequest = createRequestObj(sampleUrls)
      const testRequest: ScraperRequest = [
        {
          scraper: 'www.theglobeandmail.com',
          urls: [
            'https://www.theglobeandmail.com/canada/article-ukrainian-children-with-cancer-to-be-flown-to-toronto-hospital-for/'
          ]
        },
        {
          scraper: 'www.businessinsider.com',
          urls: [
            'https://www.businessinsider.com/private-jets-go-russia-dubai-after-putin-pledges-self-cleansing-2022-3',
            'https://www.businessinsider.com/russian-oligarch-helicopter-yacht-jets-ambramovich-isle-of-man-register-2022-3',
            'https://markets.businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3',
            'https://www.markets.businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3',
            'https://businessinsider.com/news/commodities/lumber-prices-fall-march-housing-market-cools-soaring-mortgage-rates-2022-3'
          ]
        }
      ]
      expect(scraperRequest).to.deep.equal(testRequest)
      done()

    })
  })

  describe("Test CRUD operations database", () => {
      beforeEach("Create temporary tables", (done) => {
        pool.query(
          "CREATE TEMPORARY TABLE publisher (LIKE publisher INCLUDING ALL)"
        ).then(() => {
          pool.query(
            "INSERT INTO pg_temp.publisher(id, tld, license) VALUES('6e561832-6f12-40e8-8877-32d9ef6d4d07', 'www.google.com', 'license_02')"
          ).then(() => {
            pool.query(
              "CREATE TEMPORARY TABLE article (LIKE article INCLUDING ALL)"
            ).then(() => {
              pool.query(
                "INSERT INTO pg_temp.article(id, title, url, publisher_id, date, content, expert) VALUES('d488d560-def3-4766-95e4-12065b058738', 'Test Title', 'www.google.com/path', '6e561832-6f12-40e8-8877-32d9ef6d4d07', '2022-03-06', 'This is content', 'John Doe')"
              ).then(() => {
                pool.query(
                  "CREATE TEMPORARY TABLE pg_temp.scraper_profile (LIKE scraper_profile INCLUDING ALL)"
                ).then(() => done()).catch((err) => done(err))
              }).catch((err) => done(err))
            }).catch((err) => done(err))
          }).catch((err) => done(err))
        }).catch((err) => done(err))
      })
  
      afterEach("Drop temporary tables", (done) => {
        pool.query("DROP TABLE IF EXISTS pg_temp.article").then(() => {
          pool.query("DROP TABLE IF EXISTS pg_temp.scraper_profile").then(() => {
            pool.query("DROP TABLE IF EXISTS pg_temp.publisher").then(() => done()).catch((err) => done(err))
          }).catch((err) => done(err))
        }).catch((err) => done(err))
      })

        it("Get publisher id from tld", (done) => {
          pool.query("SELECT * FROM pg_temp.publisher WHERE tld = 'www.google.com'").then(({ rows }) => {
            expect(rows[0].id).is.eq('6e561832-6f12-40e8-8877-32d9ef6d4d07')
            done()
          }).catch((err) => done(err))
        })
  
        it("Insert publisher", (done) => {
          pool.query("INSERT INTO pg_temp.publisher(tld, license) VALUES('www.test.com', false)").then(() => {
            pool.query(
              "SELECT * FROM pg_temp.publisher"
            ).then(({ rows }) => {
              expect(rows.length).is.eq(2)
              done()
            }).catch((err) => done(err))
          }).catch((err) => done(err))
        })
  
        it("Does publisher exists by tld", (done) => {
          pool.query("SELECT EXISTS (SELECT tld FROM pg_temp.publisher WHERE tld = 'www.google.com')").then(({ rows }) => {
            expect(rows[0].exists).is.eq(true)
            done()
          }).catch((err) => done(err))
        })

        it("Does article exists by url", (done) => {
          pool.query("SELECT EXISTS (SELECT url FROM pg_temp.article WHERE url = 'www.google.com/path')").then(({ rows }) => {
            expect(rows[0].exists).is.eq(true)
            done()
          }).catch((err) => done(err))
        })

        it("Get article by url", (done) => {
          pool.query("SELECT * FROM pg_temp.article WHERE url = 'www.google.com/path'").then(({ rows }) => {
            expect(rows.length).is.eq(1)
            done()
          }).catch((err) => done(err))
        })

        it("Insert article", (done) => {
          pool.query(
            "INSERT INTO pg_temp.article(id, title, url, publisher_id, date, content, expert) VALUES('e6b4d1d6-2e98-4d3e-acc9-25de53431a7d', 'Test Title', 'www.google.com/path/index', '6e561832-6f12-40e8-8877-32d9ef6d4d07', '2022-03-06', 'This is content', 'John Doe')"
          ).then(() => {
            pool.query(
              "SELECT * FROM pg_temp.article"
            ).then(({ rows }) => {
              expect(rows.length).is.eq(2)
              done()
            }).catch((err) => done(err))
          }).catch((err) => done(err))
        })

        it("Insert scraper_profile", (done) => {
          pool.query(
            "INSERT INTO pg_temp.scraper_profile(status, publisher_id) VALUES('inital', '6e561832-6f12-40e8-8877-32d9ef6d4d07')"
          ).then(() => {
            pool.query(
              "SELECT * FROM pg_temp.scraper_profile"
            ).then(({ rows }) => {
              expect(rows.length).is.eq(1)
              done()
            }).catch((err) => done(err))
          }).catch((err) => done(err))
        })
  })
})