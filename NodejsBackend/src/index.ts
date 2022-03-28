import express, { Application, Request, Response } from "express";
import cors from "cors"
import route from './routes/index'

export const app: Application = express()
const port = 4000;

// Body parsing Middleware
app.use(express.json())
app.use(cors())
app.use(express.urlencoded({ extended: true} ))

// Router
app.use(route)

try {
	app.listen(port, (): void => {
		console.log(`Connected successfully on port ${port}`)
	})
} catch (error: any) {
	console.error(`Error occured: ${error.message}`)
}