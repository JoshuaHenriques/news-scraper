import { Expert } from "./Expert";

export interface Article {
	title?: string,
	url: string,
	publisher: string,
	date?: string,
	content: string,
	expert?: Expert,
	dateScraped: string,
	dateUpdated: string
}