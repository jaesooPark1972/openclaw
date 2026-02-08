import { k as theme, p as defaultRuntime } from "./entry.js";
import "./auth-profiles-BPf6QUS2.js";
import "./agent-scope-C_O6Vpl0.js";
import "./utils-DX85MiPR.js";
import "./exec-B8JKbXKW.js";
import "./github-copilot-token-C8XFYz0i.js";
import "./config-BciOrS2p.js";
import "./manifest-registry-Bwjq9Iev.js";
import "./server-context-BFH7HB_M.js";
import "./errors-CMCg46fK.js";
import "./client-CBaY9GLK.js";
import "./call-BU7EfWsK.js";
import "./message-channel-CQ6DgRUw.js";
import { t as formatDocsLink } from "./links-B4nk2iDf.js";
import "./plugins-C3Bm-HQV.js";
import "./logging-pqyrk15z.js";
import "./accounts-ClnuDahN.js";
import "./paths-CHGbP1-A.js";
import "./routes-BWMhKDmj.js";
import "./pi-embedded-helpers-fGBveTb2.js";
import "./sandbox-Cf9YkzWv.js";
import "./channel-summary-D9NTAHkN.js";
import "./skills-Bhp0l6UK.js";
import "./redact-BICFkpn7.js";
import "./tool-display-NYQnSpdo.js";
import { t as parseTimeoutMs } from "./parse-timeout-DV8NQQWk.js";
import { t as runTui } from "./tui-Dd2oA_0i.js";

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