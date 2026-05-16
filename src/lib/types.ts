export interface RawLead {
  url: string;
  content: string;
  search_query: string;
}

export interface ScoredLead {
  company_name: string;
  website: string;
  email: string;
  phone: string;
  description: string;
  location: string;
  services: string;
  score: number;
  score_reason: string;
  source_url: string;
  scraped_at: string;
}
