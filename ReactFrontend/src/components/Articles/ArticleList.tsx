import { Article } from "../Article/Article"
import "./Articles.css"
import { Article as ArticleType } from "../../interfaces/Article";
import { useContext } from "react";
import { ArticlesContext } from "../../interfaces/ArticlesContextData";

export const ArticleList = () => {
	const { articles } = useContext(ArticlesContext)
	return (
		<section>
			<div className="container d-flex justify-content-center">
				<div className="articles">
				{ articles.map((article: ArticleType) => (<Article key={article.content} article={ article }/>)) }
				</div>
			</div>
		</section>
	)
}