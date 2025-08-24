export interface GoodreadsWrapped {
  total_books: number;
  total_read: number;
  total_toread: number;
  total_pages: number;
  total_authors: number;
  user_vs_goodreads: [number, number];
  longest_binge_session: Book[];
  impulse_reads: Book[];
}

export interface Book {
  Title: string;
  Author: string;
  DateRead?: string;
  DateAdded?: string;
  DaysBetween?: number;
}
