import "./pi-embedded-helpers-C3-CUql5.js";
import "./paths-scjhy7N2.js";
import "./agent-scope-BbT4OG2N.js";
import { R as theme, c as defaultRuntime } from "./subsystem-CAq3uyo7.js";
import "./utils-CKSrBNwq.js";
import "./exec-HEWTMJ7j.js";
import "./model-selection-DOOBF_0m.js";
import "./github-copilot-token-CnxakiSC.js";
import "./boolean-Wzu0-e0P.js";
import "./env-l7QVNj6j.js";
import "./config-Qw6Mvhjh.js";
import "./manifest-registry-D2Yntqcb.js";
import "./plugins-QJjTXliB.js";
import "./sandbox-25YuSHUe.js";
import "./chrome-D7QROrKP.js";
import "./skills-Tky2kCMO.js";
import "./routes-DqWhKjgZ.js";
import "./server-context-mXWLR983.js";
import "./message-channel-B8sq-ATS.js";
import "./logging-CY-Q5cwf.js";
import "./accounts-DzBgAM3C.js";
import "./paths-B-q1nXdY.js";
import "./redact-KzWHRS5J.js";
import "./tool-display-BEACy9rK.js";
import "./channel-summary-CGMFM3Z4.js";
import "./client-21XXC0l9.js";
import "./call-CksrEJ-J.js";
import { t as formatDocsLink } from "./links-DwjRqxgR.js";
import { t as parseTimeoutMs } from "./parse-timeout-CFqNj7No.js";
import { t as runTui } from "./tui-BeDYBuzM.js";

//#region src/cli/tui-cli.ts
function registerTuiCli(program) {
	program.command("tui").description("Open a terminal UI connected to the Gateway").option("--url <url>", "Gateway WebSocket URL (defaults to gateway.remote.url when configured)").option("--token <token>", "Gateway token (if required)").option("--password <password>", "Gateway password (if required)").option("--session <key>", "Session key (default: \"main\", or \"global\" when scope is global)").option("--deliver", "Deliver assistant replies", false).option("--thinking <level>", "Thinking level override").option("--message <text>", "Send an initial message after connecting").option("--timeout-ms <ms>", "Agent timeout in ms (defaults to agents.defaults.timeoutSeconds)").option("--history-limit <n>", "History entries to load", "200").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/tui", "docs.openclaw.ai/cli/tui")}\n`).action(async (opts) => {
		try {
			const timeoutMs = parseTimeoutMs(opts.timeoutMs);
			if (opts.timeoutMs !== void 0 && timeoutMs === void 0) defaultRuntime.error(`warning: invalid --timeout-ms "${String(opts.timeoutMs)}"; ignoring`);
			const historyLimit = Number.parseInt(String(opts.historyLimit ?? "200"), 10);
			await runTui({
				url: opts.url,
				token: opts.token,
				password: opts.password,
				session: opts.session,
				deliver: Boolean(opts.deliver),
				thinking: opts.thinking,
				message: opts.message,
				timeoutMs,
				historyLimit: Number.isNaN(historyLimit) ? void 0 : historyLimit
			});
		} catch (err) {
			defaultRuntime.error(String(err));
			defaultRuntime.exit(1);
		}
	});
}

//#endregion
export { registerTuiCli };