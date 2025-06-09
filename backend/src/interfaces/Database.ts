export interface DatabaseConfig {
  type: 'postgres' | 'mysql' | 'mongodb';
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
}

export interface DataQualityCheck {
  id: string;
  name: string;
  description: string;
  databaseId: string;
  query: string;
  threshold: number;
  schedule: string;
  lastRun?: Date;
  status?: 'passed' | 'failed' | 'pending';
}

export interface DataQualityResult {
  id: string;
  checkId: string;
  timestamp: Date;
  status: 'passed' | 'failed';
  value: number;
  metadata: Record<string, any>;
}
