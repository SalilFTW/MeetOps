import { config } from "../config.js";

class AIServiceError extends Error {
  constructor(message, status = 500, details = null) {
    super(message);
    this.name = "AIServiceError";
    this.status = status;
    this.details = details;
  }
}

async function request(endpoint, options = {}) {
  const url = `${config.aiServiceUrl}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!res.ok) {
      const errorText = await res.text();
      let errorJson = null;
      try {
        errorJson = JSON.parse(errorText);
      } catch {
        // ignore
      }
      throw new AIServiceError(
        errorJson?.detail || errorJson?.message || `AI Service request failed with status ${res.status}`,
        res.status,
        errorJson || errorText
      );
    }

    return await res.json();
  } catch (err) {
    if (err instanceof AIServiceError) {
      throw err;
    }
    throw new AIServiceError(
      `Could not communicate with AI Service at ${config.aiServiceUrl}: ${err.message}`,
      503,
      { originalError: err.message }
    );
  }
}

export const aiClient = {
  async checkHealth() {
    return request("/health");
  },

  async runPipeline({ use_llm = false, brief_date = null } = {}) {
    return request("/ai/pipeline/run", {
      method: "POST",
      body: JSON.stringify({
        use_llm,
        brief_date,
      }),
    });
  },

  async extractActions({ use_llm = false, resolve_duplicates = true } = {}) {
    const query = new URLSearchParams({
      use_llm: String(use_llm),
      resolve_duplicates: String(resolve_duplicates),
    });
    return request(`/ai/actions?${query}`);
  },

  async resolveActions(actions) {
    return request("/ai/resolve", {
      method: "POST",
      body: JSON.stringify({ actions }),
    });
  },

  async buildDailyBrief(actions, briefDate = null) {
    return request("/ai/brief", {
      method: "POST",
      body: JSON.stringify({
        actions,
        brief_date: briefDate,
      }),
    });
  },
};
