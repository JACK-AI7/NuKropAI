import { Router, type IRouter } from "express";
import healthRouter from "./health";
import chatRouter from "./chat";
import scanRouter from "./scan";
import voiceRouter from "./voice";
import weatherRouter from "./weather";
import marketRouter from "./market";
import alertsRouter from "./alerts";

const router: IRouter = Router();

router.use(healthRouter);
router.use(chatRouter);
router.use(scanRouter);
router.use(voiceRouter);
router.use(weatherRouter);
router.use(marketRouter);
router.use(alertsRouter);

export default router;
