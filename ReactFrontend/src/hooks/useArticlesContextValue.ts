import { useCallback, useState } from "react";
import { Article } from "../interfaces/Article";
import { ArticlesContextData } from "../interfaces/ArticlesContextData";

export const useArticlesContextValue = (): ArticlesContextData => {
	const [articles, setArticles] = useState<Article[]>([])

	const scrapeArticles = useCallback(async (urls: string) => {
		// Maybe try React Query?
		const parsedUrls: string[] = urls.split('\n')
		try {
			const res = await fetch('http://localhost:4000/scrapeArticles', {
				method: "POST",
				body: JSON.stringify({
					urls: parsedUrls
				}),
				headers: {
				"Access-Control-Allow-Origin": "*",
				"Content-type": "application/json"
				},
			})
			const data = await res.json()
			console.log(data)
			setArticles(data.articles)
		} catch(e) {
			console.log(e)
		}
	  }, [setArticles])
	return { articles, scrapeArticles }
}