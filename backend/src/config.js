import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "../..");

dotenv.config({ path: path.join(rootDir, ".env") });

export const config = {
  port: parseInt(process.env.PORT || "3000", 10),
  aiServiceUrl: process.env.AI_SERVICE_URL || "http://127.0.0.1:8000",
  dbPath: process.env.DB_PATH || path.resolve(rootDir, "data/meetops.db"),
  appName: process.env.APP_NAME || "MeetOps",
  executiveName: "Arjun Malhotra",
};
