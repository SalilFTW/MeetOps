import express from "express";
import { aiClient } from "../services/aiClient.js";

const router = express.Router();

router.post("/ask", async (req, res) => {
  try {
    const { question } = req.body;

    if (!question || typeof question !== "string") {
      return res.status(400).json({
        error: "Question is required",
      });
    }

    const result = await aiClient.askQuestion(question);

    return res.json(result);
  } catch (err) {
    console.error("Q&A route error:", err);

    return res.status(err.status || 500).json({
      error: err.message || "Failed to answer question",
      details: err.details || null,
    });
  }
});

export { router as qaRoutes };