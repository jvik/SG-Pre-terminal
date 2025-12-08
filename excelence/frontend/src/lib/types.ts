export interface Category {
  id: string; // Assuming UUIDs are strings
  name: string;
  emoji?: string;
}

export interface Transaction {
  id: string; // Assuming UUIDs are strings
  amount: number;
  type: 'income' | 'expense';
  date: string; // Dates will be strings in ISO format
  description: string | null;
  user_id: string;
  category_id: string;
}
