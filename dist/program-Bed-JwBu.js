import { C as setVerbose, O as isRich, k as theme, n as isTruthyEnvValue, p as defaultRuntime } from "./entry.js";
import "./auth-profiles-BPf6QUS2.js";
import { n as replaceCliName, r as resolveCliName } from "./command-format-ayFsmwwz.js";
import "./agent-scope-C_O6Vpl0.js";
import "./utils-DX85MiPR.js";
import "./exec-B8JKbXKW.js";
import "./github-copilot-token-C8XFYz0i.js";
import "./pi-model-discovery-DsRqYJLy.js";
import { j as VERSION } from "./config-BciOrS2p.js";
import "./manifest-registry-Bwjq9Iev.js";
import "./server-context-BFH7HB_M.js";
import "./errors-CMCg46fK.js";
import "./control-service-BdPnWu68.js";
import "./tailscale-DCnMs7_q.js";
import "./auth-nnRYiqpH.js";
import "./client-CBaY9GLK.js";
import "./call-BU7EfWsK.js";
import "./message-channel-CQ6DgRUw.js";
import { t as formatDocsLink } from "./links-B4nk2iDf.js";
import "./plugin-auto-enable-NjMc48wv.js";
import "./plugins-C3Bm-HQV.js";
import "./logging-pqyrk15z.js";
import "./accounts-ClnuDahN.js";
import "./loader-B-fEgzCz.js";
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
import { n as resolveCliChannelOptions } from "./channel-options-B-tYLnGt.js";
import { a as getCommandPath, d as hasHelpOrVersion, l as getVerboseFlag } from "./register.subclis-B7EvLlxy.js";
import "./completion-cli-BzY-E2tK.js";
import "./gateway-rpc-DsifQTWk.js";
import "./deps-D1H89A9U.js";
import "./daemon-runtime-C1I751F4.js";
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
import { t as forceFreePort } from "./ports-C0cgmLqb.js";
import "./auth-health-D0F5qv8z.js";
import { i as hasEmittedCliBanner, n as emitCliBanner, o as registerProgramCommands, r as formatCliBannerLine, t as ensureConfigReady } from "./config-guard-CyPtO4wa.js";
import "./help-format-Dm3Y6bcY.js";
import "./configure-8yVdL7yQ.js";
import "./systemd-linger-C6GGQ-sU.js";
import "./doctor-D10tTcRF.js";
import { Command } from "commander";

//#region src/cli/program/context.ts
function createProgramContext() {
	const channelOptions = resolveCliChannelOptions();
	return {
		programVersion: VERSION,
		channelOptions,
		messageChannelOptions: channelOptions.join("|"),
		agentChannelOptions: ["last", ...channelOptions].join("|")
	};
}

//#endregion
//#region src/cli/program/help.ts
const CLI_NAME = resolveCliName();
const EXAMPLES = [
	["openclaw channels login --verbose", "Link personal WhatsApp Web and show QR + connection logs."],
	["openclaw message send --target +15555550123 --message \"Hi\" --json", "Send via your web session and print JSON result."],
	["openclaw gateway --port 18789", "Run the WebSocket Gateway locally."],
	["openclaw --dev gateway", "Run a dev Gateway (isolated state/config) on ws://127.0.0.1:19001."],
	["openclaw gateway --force", "Kill anything bound to the default gateway port, then start it."],
	["openclaw gateway ...", "Gateway control via WebSocket."],
	["openclaw agent --to +15555550123 --message \"Run summary\" --deliver", "Talk directly to the agent using the Gateway; optionally send the WhatsApp reply."],
	["openclaw message send --channel telegram --target @mychat --message \"Hi\"", "Send via your Telegram bot."]
];
function configureProgramHelp(program, ctx) {
	program.name(CLI_NAME).description("").version(ctx.programVersion).option("--dev", "Dev profile: isolate state under ~/.openclaw-dev, default gateway port 19001, and shift derived ports (browser/canvas)").option("--profile <name>", "Use a named profile (isolates OPENCLAW_STATE_DIR/OPENCLAW_CONFIG_PATH under ~/.openclaw-<name>)");
	program.option("--no-color", "Disable ANSI colors", false);
	program.configureHelp({
		optionTerm: (option) => theme.option(option.flags),
		subcommandTerm: (cmd) => theme.command(cmd.name())
	});
	program.configureOutput({
		writeOut: (str) => {
			const colored = str.replace(/^Usage:/gm, theme.heading("Usage:")).replace(/^Options:/gm, theme.heading("Options:")).replace(/^Commands:/gm, theme.heading("Commands:"));
			process.stdout.write(colored);
		},
		writeErr: (str) => process.stderr.write(str),
		outputError: (str, write) => write(theme.error(str))
	});
	if (process.argv.includes("-V") || process.argv.includes("--version") || process.argv.includes("-v")) {
		console.log(ctx.programVersion);
		process.exit(0);
	}
	program.addHelpText("beforeAll", () => {
		if (hasEmittedCliBanner()) return "";
		const rich = isRich();
		return `\n${formatCliBannerLine(ctx.programVersion, { richTty: rich })}\n`;
	});
	const fmtExamples = EXAMPLES.map(([cmd, desc]) => `  ${theme.command(replaceCliName(cmd, CLI_NAME))}\n    ${theme.muted(desc)}`).join("\n");
	program.addHelpText("afterAll", ({ command }) => {
		if (command !== program) return "";
		const docs = formatDocsLink("/cli", "docs.openclaw.ai/cli");
		return `\n${theme.heading("Examples:")}\n${fmtExamples}\n\n${theme.muted("Docs:")} ${docs}\n`;
	});
}

//#endregion
//#region src/cli/program/preaction.ts
function setProcessTitleForCommand(actionCommand) {
	let current = actionCommand;
	while (current.parent && current.parent.parent) current = current.parent;
	const name = current.name();
	const cliName = resolveCliName();
	if (!name || name === cliName) return;
	process.title = `${cliName}-${name}`;
}
const PLUGIN_REQUIRED_COMMANDS = new Set([
	"message",
	"channels",
	"directory"
]);
function registerPreActionHooks(program, programVersion) {
	program.hook("preAction", async (_thisCommand, actionCommand) => {
		setProcessTitleForCommand(actionCommand);
		const argv = process.argv;
		if (hasHelpOrVersion(argv)) return;
		const commandPath = getCommandPath(argv, 2);
		if (!(isTruthyEnvValue(process.env.OPENCLAW_HIDE_BANNER) || commandPath[0] === "update" || commandPath[0] === "completion" || commandPath[0] === "plugins" && commandPath[1] === "update")) emitCliBanner(programVersion);
		const verbose = getVerboseFlag(argv, { includeDebug: true });
		setVerbose(verbose);
		if (!verbose) process.env.NODE_NO_WARNINGS ??= "1";
		if (commandPath[0] === "doctor" || commandPath[0] === "completion") return;
		await ensureConfigReady({
			runtime: defaultRuntime,
			commandPath
		});
		if (PLUGIN_REQUIRED_COMMANDS.has(commandPath[0])) ensurePluginRegistryLoaded();
	});
}

//#endregion
//#region src/cli/program/build-program.ts
function buildProgram() {
	const program = new Command();
	const ctx = createProgramContext();
	const argv = process.argv;
	configureProgramHelp(program, ctx);
	registerPreActionHooks(program, ctx.programVersion);
	registerProgramCommands(program, ctx, argv);
	return program;
}

//#endregion
export { buildProgram };