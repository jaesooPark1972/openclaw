import { c as enableConsoleCapture, i as normalizeEnv, n as isTruthyEnvValue, p as defaultRuntime } from "./entry.js";
import "./auth-profiles-BPf6QUS2.js";
import "./agent-scope-C_O6Vpl0.js";
import { d as resolveConfigDir } from "./utils-DX85MiPR.js";
import "./exec-B8JKbXKW.js";
import "./github-copilot-token-C8XFYz0i.js";
import "./pi-model-discovery-DsRqYJLy.js";
import { j as VERSION } from "./config-BciOrS2p.js";
import "./manifest-registry-Bwjq9Iev.js";
import "./server-context-BFH7HB_M.js";
import { r as formatUncaughtError } from "./errors-CMCg46fK.js";
import "./control-service-BdPnWu68.js";
import { t as ensureOpenClawCliOnPath } from "./path-env-DEj4CiFN.js";
import "./tailscale-DCnMs7_q.js";
import "./auth-nnRYiqpH.js";
import "./client-CBaY9GLK.js";
import "./call-BU7EfWsK.js";
import "./message-channel-CQ6DgRUw.js";
import "./links-B4nk2iDf.js";
import "./plugin-auto-enable-NjMc48wv.js";
import "./plugins-C3Bm-HQV.js";
import "./logging-pqyrk15z.js";
import "./accounts-ClnuDahN.js";
import { jt as installUnhandledRejectionHandler } from "./loader-B-fEgzCz.js";
import "./progress-Bcjniu7m.js";
import "./prompt-style-CFsleyxV.js";
import "./note-_C44YfAQ.js";
import "./clack-prompter-B9yLhyOm.js";
import "./onboard-channels-B65gOZiU.js";
import "./archive-ccN9aDgq.js";
import "./installs-BP4K5L33.js";
import "./manager-B6hhnrCh.js";
import "./paths-CHGbP1-A.js";
import "./sqlite-CmdZSZRx.js";
import "./routes-BWMhKDmj.js";
import "./pi-embedded-helpers-fGBveTb2.js";
import "./deliver-BMXqaGzB.js";
import "./sandbox-Cf9YkzWv.js";
import "./channel-summary-D9NTAHkN.js";
import "./wsl-Bqq-vg2h.js";
import "./skills-Bhp0l6UK.js";
import "./image-BC3yWlpT.js";
import "./redact-BICFkpn7.js";
import "./tool-display-NYQnSpdo.js";
import "./restart-sentinel-Cr0vUxB8.js";
import "./channel-selection-BuvOKotO.js";
import "./commands-CR6ee-_d.js";
import "./pairing-store-DRn08lZD.js";
import "./login-qr-C_8cc5TO.js";
import "./pairing-labels-Ds7BPOkj.js";
import "./channels-status-issues-ZcR1U-m5.js";
import { n as ensurePluginRegistryLoaded } from "./command-options-D_-qdSoI.js";
import { a as getCommandPath, c as getPrimaryCommand, d as hasHelpOrVersion } from "./register.subclis-B7EvLlxy.js";
import "./completion-cli-BzY-E2tK.js";
import "./gateway-rpc-DsifQTWk.js";
import "./deps-D1H89A9U.js";
import "./daemon-runtime-C1I751F4.js";
import { t as assertSupportedRuntime } from "./runtime-guard-X5t_VXaZ.js";
import "./service-2b1kQ450.js";
import "./systemd-BJ-PZAXC.js";
import "./service-audit-ACLEyCEM.js";
import "./table-2ulSuXr0.js";
import "./widearea-dns-DHQx96_K.js";
import "./audit-CzFjZ0nl.js";
import "./onboard-skills-Dnvd2qXm.js";
import "./health-format-DoimNs4E.js";
import "./update-runner-CQHkL_bo.js";
import "./github-copilot-auth-Bhyh_ClQ.js";
import "./logging-C6k_H0a0.js";
import "./hooks-status-B6XRTrOh.js";
import "./status-Da5XGaAF.js";
import "./skills-status-68SV0Ams.js";
import "./tui-Dd2oA_0i.js";
import "./agent-CbaQyZNj.js";
import "./node-service-Cy7Xs3vY.js";
import "./status.update-Bk45TwI4.js";
import "./auth-health-D0F5qv8z.js";
import { a as findRoutedCommand, n as emitCliBanner, t as ensureConfigReady } from "./config-guard-CyPtO4wa.js";
import "./help-format-Dm3Y6bcY.js";
import "./configure-8yVdL7yQ.js";
import "./systemd-linger-C6GGQ-sU.js";
import "./doctor-D10tTcRF.js";
import path from "node:path";
import process$1 from "node:process";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

//#region src/infra/dotenv.ts
function loadDotEnv(opts) {
	const quiet = opts?.quiet ?? true;
	dotenv.config({ quiet });
	const globalEnvPath = path.join(resolveConfigDir(process.env), ".env");
	if (!fs.existsSync(globalEnvPath)) return;
	dotenv.config({
		quiet,
		path: globalEnvPath,
		override: false
	});
}

//#endregion
//#region src/cli/route.ts
async function prepareRoutedCommand(params) {
	emitCliBanner(VERSION, { argv: params.argv });
	await ensureConfigReady({
		runtime: defaultRuntime,
		commandPath: params.commandPath
	});
	if (params.loadPlugins) ensurePluginRegistryLoaded();
}
async function tryRouteCli(argv) {
	if (isTruthyEnvValue(process.env.OPENCLAW_DISABLE_ROUTE_FIRST)) return false;
	if (hasHelpOrVersion(argv)) return false;
	const path = getCommandPath(argv, 2);
	if (!path[0]) return false;
	const route = findRoutedCommand(path);
	if (!route) return false;
	await prepareRoutedCommand({
		argv,
		commandPath: path,
		loadPlugins: route.loadPlugins
	});
	return route.run(argv);
}

//#endregion
//#region src/cli/run-main.ts
function rewriteUpdateFlagArgv(argv) {
	const index = argv.indexOf("--update");
	if (index === -1) return argv;
	const next = [...argv];
	next.splice(index, 1, "update");
	return next;
}
async function runCli(argv = process$1.argv) {
	const normalizedArgv = stripWindowsNodeExec(argv);
	loadDotEnv({ quiet: true });
	normalizeEnv();
	ensureOpenClawCliOnPath();
	assertSupportedRuntime();
	if (await tryRouteCli(normalizedArgv)) return;
	enableConsoleCapture();
	const { buildProgram } = await import("./program-Bed-JwBu.js");
	const program = buildProgram();
	installUnhandledRejectionHandler();
	process$1.on("uncaughtException", (error) => {
		console.error("[openclaw] Uncaught exception:", formatUncaughtError(error));
		process$1.exit(1);
	});
	const parseArgv = rewriteUpdateFlagArgv(normalizedArgv);
	const primary = getPrimaryCommand(parseArgv);
	if (primary) {
		const { registerSubCliByName } = await import("./register.subclis-B7EvLlxy.js").then((n) => n.i);
		await registerSubCliByName(program, primary);
	}
	if (!(!primary && hasHelpOrVersion(parseArgv))) {
		const { registerPluginCliCommands } = await import("./cli-eN9ygnpi.js");
		const { loadConfig } = await import("./config-BciOrS2p.js").then((n) => n.t);
		registerPluginCliCommands(program, loadConfig());
	}
	await program.parseAsync(parseArgv);
}
function stripWindowsNodeExec(argv) {
	if (process$1.platform !== "win32") return argv;
	const stripControlChars = (value) => {
		let out = "";
		for (let i = 0; i < value.length; i += 1) {
			const code = value.charCodeAt(i);
			if (code >= 32 && code !== 127) out += value[i];
		}
		return out;
	};
	const normalizeArg = (value) => stripControlChars(value).replace(/^['"]+|['"]+$/g, "").trim();
	const normalizeCandidate = (value) => normalizeArg(value).replace(/^\\\\\\?\\/, "");
	const execPath = normalizeCandidate(process$1.execPath);
	const execPathLower = execPath.toLowerCase();
	const execBase = path.basename(execPath).toLowerCase();
	const isExecPath = (value) => {
		if (!value) return false;
		const normalized = normalizeCandidate(value);
		if (!normalized) return false;
		const lower = normalized.toLowerCase();
		return lower === execPathLower || path.basename(lower) === execBase || lower.endsWith("\\node.exe") || lower.endsWith("/node.exe") || lower.includes("node.exe") || path.basename(lower) === "node.exe" && fs.existsSync(normalized);
	};
	const filtered = argv.filter((arg, index) => index === 0 || !isExecPath(arg));
	if (filtered.length < 3) return filtered;
	const cleaned = [...filtered];
	if (isExecPath(cleaned[1])) cleaned.splice(1, 1);
	if (isExecPath(cleaned[2])) cleaned.splice(2, 1);
	return cleaned;
}

//#endregion
export { runCli };