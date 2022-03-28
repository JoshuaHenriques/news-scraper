import "bootstrap/dist/css/bootstrap.min.css";

import { ScrapeForm } from "./components/ScrapeForm/ScrapeForm";
import { Header } from "./components/Header/Header";
import { ArticlesContext } from "./interfaces/ArticlesContextData";
import { ArticleList } from "./components/Articles/ArticleList";
import { useArticlesContextValue } from "./hooks/useArticlesContextValue";

export const App = () => {
  const articlesContextValue = useArticlesContextValue()

  return (
    <ArticlesContext.Provider value={articlesContextValue}>
      <Header />
      <ScrapeForm />
      <ArticleList />
      {/* <Pagination nextPage={nextPage} prevPage={prevPage} /> */}
      {/* <Footer /> */}
    </ArticlesContext.Provider>
  );
};

export default App;
