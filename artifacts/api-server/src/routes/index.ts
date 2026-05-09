import { Router, type IRouter } from "express";
import healthRouter from "./health";
import chatRouter from "./chat";
import scanRouter from "./scan";

const router: IRouter = Router();

router.use(healthRouter);
router.use(chatRouter);
router.use(scanRouter);

export default router;
