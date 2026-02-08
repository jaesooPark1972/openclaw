import { o as createSubsystemLogger } from "./entry.js";
import "./auth-profiles-BPf6QUS2.js";
import { c as resolveDefaultAgentId, s as resolveAgentWorkspaceDir } from "./agent-scope-C_O6Vpl0.js";
import "./utils-DX85MiPR.js";
import "./exec-B8JKbXKW.js";
import "./github-copilot-token-C8XFYz0i.js";
import "./pi-model-discovery-DsRqYJLy.js";
import { i as loadConfig } from "./config-BciOrS2p.js";
import "./manifest-registry-Bwjq9Iev.js";
import "./server-context-BFH7HB_M.js";
import "./errors-CMCg46fK.js";
import "./control-service-BdPnWu68.js";
import "./client-CBaY9GLK.js";
import "./call-BU7EfWsK.js";
import "./message-channel-CQ6DgRUw.js";
import "./links-B4nk2iDf.js";
import "./plugins-C3Bm-HQV.js";
import "./logging-pqyrk15z.js";
import "./accounts-ClnuDahN.js";
import { t as loadOpenClawPlugins } from "./loader-B-fEgzCz.js";
import "./progress-Bcjniu7m.js";
import "./prompt-style-CFsleyxV.js";
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

//#region src/plugins/cli.ts
const log = createSubsystemLogger("plugins");
function registerPluginCliCommands(program, cfg) {
	const config = cfg ?? loadConfig();
	const workspaceDir = resolveAgentWorkspaceDir(config, resolveDefaultAgentId(config));
	const logger = {
		info: (msg) => log.info(msg),
		warn: (msg) => log.warn(msg),
		error: (msg) => log.error(msg),
		debug: (msg) => log.debug(msg)
	};
	const registry = loadOpenClawPlugins({
		config,
		workspaceDir,
		logger
	});
	const existingCommands = new Set(program.commands.map((cmd) => cmd.name()));
	for (const entry of registry.cliRegistrars) {
		if (entry.commands.length > 0) {
			const overlaps = entry.commands.filter((command) => existingCommands.has(command));
			if (overlaps.length > 0) {
				log.debug(`plugin CLI register skipped (${entry.pluginId}): command already registered (${overlaps.join(", ")})`);
				continue;
			}
		}
		try {
			const result = entry.register({
				program,
				config,
				workspaceDir,
				logger
			});
			if (result && typeof result.then === "function") result.catch((err) => {
				log.warn(`plugin CLI register failed (${entry.pluginId}): ${String(err)}`);
			});
			for (const command of entry.commands) existingCommands.add(command);
		} catch (err) {
			log.warn(`plugin CLI register failed (${entry.pluginId}): ${String(err)}`);
		}
	}
}

//#endregion
export { registerPluginCliCommands };