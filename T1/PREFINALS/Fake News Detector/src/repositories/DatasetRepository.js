import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import PickleLoader from "../services/PickleLoaderService.js";

export class DatasetRepository {
  constructor(options = {}) {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    this.dataDir = options.dataDir || path.join(__dirname, "../../data");
    this.samplePerCsv = options.samplePerCsv;
  }

  async #loadPickle(filePath) {
    try {
      const data = await PickleLoader.loadPickle(filePath);
      
      // Apply sample limit if specified
      if (Number.isFinite(this.samplePerCsv) && this.samplePerCsv > 0) {
        return data.slice(0, this.samplePerCsv);
      }
      
      return data;
    } catch (error) {
      console.error(`Error loading pickle file ${filePath}:`, error);
      throw error;
    }
  }

  async loadAll() {
    const truePicklePath = path.join(this.dataDir, "True.pkl");
    const fakePicklePath = path.join(this.dataDir, "Fake.pkl");
    const real = await this.#loadPickle(truePicklePath);
    const fake = await this.#loadPickle(fakePicklePath);
    return [...real, ...fake];
  }
}


