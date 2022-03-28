import { Article as ArticleType } from "../../interfaces/Article";

export const Article = ( { article }: { article: ArticleType }) => {
	return (
		<section>
			<div className="card my-5" >
				<div className="card-body">
					<h4 className="card-title">{ article.title }</h4>
					<p>Expert: { article.expert ? article.expert : 'Not Scraped' }</p>
					<p>Date: { article.date ? article.date : 'Not Scraped'}</p>
					<p>{ article.url }</p>
					<p className="card-text">{ article.content }</p>
					<a href={ article.url } rel="noreferrer" target="_blank" className="btn btn-primary">Go to Article</a>
				</div>
			</div>
		</section>
	)
}