const API_BASE_URL = "http://127.0.0.1:3000/api";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type") || "";

  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof data === "object" && data?.error
        ? data.error
        : `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data;
}

export const api = {
  // --------------------------------------------------
  // Health
  // --------------------------------------------------

  async getHealth() {
    return request("/health");
  },

  // --------------------------------------------------
  // Actions
  // --------------------------------------------------

  async getActions(filters = {}) {
    const params = new URLSearchParams();

    if (filters.ownership) {
      params.set("ownership", filters.ownership);
    }

    if (filters.status) {
      params.set("status", filters.status);
    }

    if (filters.owner) {
      params.set("owner", filters.owner);
    }

    const query = params.toString();

    return request(`/actions${query ? `?${query}` : ""}`);
  },

  async getAction(id) {
    return request(`/actions/${id}`);
  },

  async updateActionStatus(id, status) {
    return request(`/actions/${id}`, {
      method: "PATCH",
      body: JSON.stringify({
        status,
      }),
    });
  },

  // --------------------------------------------------
  // Daily Brief
  // --------------------------------------------------

  async getLatestBrief() {
    return request("/briefs/latest");
  },

  async getBriefByDate(date) {
    return request(`/briefs/${date}`);
  },

  // --------------------------------------------------
  // Conflicts
  // --------------------------------------------------

  async getConflicts(resolved) {
    const params = new URLSearchParams();

    if (resolved !== undefined && resolved !== null) {
      params.set("resolved", String(resolved));
    }

    const query = params.toString();

    return request(`/conflicts${query ? `?${query}` : ""}`);
  },

  async resolveConflict(id) {
    return request(`/conflicts/${id}/resolve`, {
      method: "POST",
    });
  },

  // --------------------------------------------------
  // Pipeline
  // --------------------------------------------------

  async runPipeline({
    use_llm = false,
    brief_date = null,
  } = {}) {
    return request("/pipeline/run", {
      method: "POST",
      body: JSON.stringify({
        use_llm,
        brief_date,
      }),
    });
  },

  // --------------------------------------------------
  // Ask MeetOps
  // --------------------------------------------------

  async askMeetOps(question) {
    return request("/ask", {
      method: "POST",
      body: JSON.stringify({
        question,
      }),
    });
  },
};