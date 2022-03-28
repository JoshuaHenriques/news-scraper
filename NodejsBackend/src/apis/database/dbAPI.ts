import { URL } from "url";
import { Article } from "../../types/entities/Article";

// Should this be a class? Probably

const pgp = require("pg-promise")();

// DEPLOYMENT CONCERN!!!!!!!
const db = pgp("postgres://postgres:example@localhost:5432/postgres");



// Better function names: hasArticleBeenCached, hasUrlBeenCached

/**
 * Queries the database to check if article with given url has already been scraped.
 * @param url   url to check
 * @returns boolean
 */
export const hasUrlBeenScraped = async (url: string): Promise<boolean> => {
  var beenScraped: boolean = false;
  await db
    .one('SELECT EXISTS(select 1 from article where url=$1)', [url])
    .then((data: any) => {
      beenScraped = data.exists;
    });
  return beenScraped;
};




// Is tld a better var name than publisherName? 
//    This applies to getInsertPublisher as well
// Better function name: hasPublisherBeenCached

/**
 * Queries the database to check if the publisher exists on the DB
 * @param publisherName The tld of the publisher.
 * @returns a promised boolean of validity
 */
export const isValidPublisher = async (publisherName: string): Promise<boolean> => {
  var validity: boolean = false;
  await db
    .one("SELECT EXISTS(select 1 from publisher where name=$1)", [
      publisherName,
    ])
    .then((data: any) => {
      validity = data.exists;
    });
  return validity;
};


/**
 * Attempts to get a publisherID given the name/tld. If none are found, Insert it
 * @param publisherName The tld of the publisher
 * @returns the publisher_id of the publisher
 */
export const getInsertPublisher = async (publisherName: string):Promise <any> => {
  return db.task("getInsertUserId", async (t: any) => {
    const publisherId = await t.oneOrNone(
      "SELECT id FROM publisher WHERE tld = $1",
      [publisherName],
      (u: { id: any }) => u && u.id
    );
    return (
      (await publisherId) ||
      (await t.one(
        "INSERT INTO publisher(tld) VALUES($1) RETURNING id",
        [publisherName],
        (u: { id: any }) => u.id
      ))
    );
  });
};

/**
 * Inserts an article into the database
 * @param article The article to be inserted
 * @param publisherId The publisher_id of the publisher that published it
 */
export const insertArticle = async (article: Article, publisherId: string):Promise <void> =>{
  await db.none(
    "INSERT INTO article(publisher_id, url, content, title, expert, date) VALUES($1, $2, $3, $4, $5, $6) ",
    [
      publisherId,
      article.url,
      article.content,
      article.title,
      article.expert,
      article.date,
    ]
  );
};

/**
 * Retrieves a list of articles from db
 * @param urls Array of urls to fetch
 * @returns A promised array of articles
 */
export const retrieveCachedArticles = async (urls: string[]): Promise <Article[]> => {
  const cachedArticles: Article[] = [];

  const retrievedURL = Promise.all(
    urls.map(async (url: string) => {
      await db
        .one("SELECT * FROM article where url=($1)", [url])
        .then((data: any) => {

          
          // Unsure if this is good practice or if branches are necessary for error checking.
          // If the fields aren't there we have a bigger problem.
          //   Alternative could be:
          //    can the fields be ommited from within the query?

          if (data.created_at) {
            delete data.created_at;
          }
          if (data.updated_at) {
            delete data.updated_at;
          }
          if (data.id) {
            delete data.id;
          }
          if (data.publisher_id) {
            delete data.publisher_id;
          }

          data.title += "  [TAKEN FROM DATABASE]";

          cachedArticles.push(data);
        });
    })
  );

  await retrievedURL;
  return cachedArticles;
};

/**
 * Stores articles in the database
 * @param scrapedArticles List of articles to be inserted
 */
export const cacheScrapedArticles = async (scrapedArticles: Article[]): Promise<void> => {
  for (const article of scrapedArticles) {
    const publisherId = await getInsertPublisher(
      extractHostNameFromUrl(article.url)
    );
    if (await hasUrlBeenScraped(article.url)) {
      return;
    } else {
      insertArticle(article, publisherId);
    }
  }
};

/**
 * Extracts the tld from a url
 * @param url url to be harvested
 * @returns the tld
 */
export const extractHostNameFromUrl = (url: string): string => {
  const urlObj = new URL(url);
  return urlObj.hostname;
};
