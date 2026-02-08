import "./pi-embedded-helpers-C3-CUql5.js";
import { Z as loadOpenClawPlugins } from "./reply-C5JNwqud.js";
import "./paths-scjhy7N2.js";
import { c as resolveDefaultAgentId, s as resolveAgentWorkspaceDir } from "./agent-scope-BbT4OG2N.js";
import { t as createSubsystemLogger } from "./subsystem-CAq3uyo7.js";
import "./utils-CKSrBNwq.js";
import "./exec-HEWTMJ7j.js";
import "./model-selection-DOOBF_0m.js";
import "./github-copilot-token-CnxakiSC.js";
import "./boolean-Wzu0-e0P.js";
import "./env-l7QVNj6j.js";
import { i as loadConfig } from "./config-Qw6Mvhjh.js";
import "./manifest-registry-D2Yntqcb.js";
import "./plugins-QJjTXliB.js";
import "./sandbox-25YuSHUe.js";
import "./image-DYABHo2D.js";
import "./pi-model-discovery-B6CsmK6Y.js";
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
import "./deliver-DZYm5jjB.js";
import "./dispatcher-65cJh64S.js";
import "./manager-BbS_sIb-.js";
import "./sqlite-QDf0yuU0.js";
import "./channel-summary-CGMFM3Z4.js";
import "./client-21XXC0l9.js";
import "./call-CksrEJ-J.js";
import "./login-qr-BKgUFXKH.js";
import "./pairing-store-DDLNuzmx.js";
import "./links-DwjRqxgR.js";
import "./progress-CvaSPjS9.js";
import "./pi-tools.policy-kBs98K-U.js";
import "./prompt-style-DYJdrXyV.js";
import "./pairing-labels-ClZ-fTWT.js";
import "./control-service-GNJdHKwJ.js";
import "./restart-sentinel-DUemCjgU.js";
import "./channel-selection-C2oqOL_H.js";

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