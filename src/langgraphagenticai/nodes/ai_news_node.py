from tavily import TavilyClient
import os

class AINewsNode:
    def __init__(self,llm):
        """Initailize the AINewsNode with APIU keys for Tavily and GROQ."""
        self.tavily_client = TavilyClient()
        self.llm=llm

        #this is used to capture various steps in the file so that later can be use for steps  shown
        self.state ={}

    def fetch_news(self,state:dict) ->dict:
        """ 
        Fetch AI news based on the specified frequency.
        
        Args:        state (dict): A dictionary containing 'frequency'.
        
        Returns:  dict: Updated state with 'news_data' key containing fetched news.
        """
        frequency = (state.get('frequency') or 'Daily').lower()
        query = state.get('query') or "Latest Artificial Intelligence news worldwide"
        self.state["frequency"]=frequency

        response = self.tavily_client.search(
            query=query,
            max_results=12,
            search_depth="advanced",
        )
        state['news_data']=response.get("results",[])
        self.state["news_data"]=state['news_data']
        return state
    
    def summerize_news(self,state:dict) -> dict:
        """ Sumerize the fetched news using an LLM.
        
        Args:        state (dict): A dictionary containing 'news_data'. 
        
        Returns:  dict: Updated state with 'summary' key containing the summarized news.
        """


        news_items = self.state['news_data']

        articles = []
        for item in news_items:
            title = item.get('title','')
            content = item.get('content','')
            url = item.get('url','')
            date = item.get('published_date','') or item.get('published_at','')
            articles.append(f"Title: {title}\nDate: {date}\nURL: {url}\nContent: {content}")
        articles_str = "\n\n".join(articles)

        prompt_text = (
            "Summarize the following AI news into Markdown. For each item include:\n"
            "- Date in YYYY-MM-DD (latest first)\n"
            "- 1–2 concise sentences\n"
            "- Source URL as a link\n\n"
            "Articles:\n" + articles_str
        )

        response = self.llm.invoke([{"role": "user", "content": prompt_text}])
        summary = getattr(response, "content", str(response))
        state['summary']=summary
        self.state["summary"]=state['summary']
        return self.state
    

    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_ai_news_summary.md"
        os.makedirs("./AINews", exist_ok=True)
        with open(filename, "w") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n{summary}")
        self.state["filename"]=filename
        return self.state
