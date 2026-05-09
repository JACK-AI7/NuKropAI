import type { Request, Response } from "express";
import { Router } from "express";
import multer from "multer";
import { toFile } from "openai";
import { openai } from "@workspace/integrations-openai-ai-server";

const voiceRouter = Router();
const upload = multer({ storage: multer.memoryStorage() });

voiceRouter.post(
  "/voice",
  upload.single("audio"),
  async (req: Request, res: Response) => {
    if (!req.file?.buffer?.length) {
      res.status(400).json({ error: "No audio file received" });
      return;
    }

    const mimeType = req.file.mimetype || "audio/m4a";
    const filename = req.file.originalname || "recording.m4a";

    try {
      const audioFile = await toFile(req.file.buffer, filename, {
        type: mimeType,
      });

      const transcription = await openai.audio.transcriptions.create({
        file: audioFile,
        model: "whisper-1",
      });

      res.json({ text: transcription.text ?? "" });
    } catch (err) {
      req.log.error({ err }, "Voice transcription failed");
      res.status(500).json({ error: "Transcription failed. Please try again." });
    }
  }
);

export default voiceRouter;
