const path = require('path');
const bindings = require('bindings');

// Load the native addon
// bindings() tries to find the built .node file in standardized locations
const addon = bindings('bio_audio_engine');

module.exports = {
    /**
     * Checks if a frequency is within the human vocal range.
     * @param {number} frequencyInHz 
     * @returns {boolean}
     */
    checkVocalPlausibility: addon.checkVocalPlausibility,

    /**
     * Placeholder for the main audio processing pipeline.
     * @returns {string} Status message
     */
    processAudio: addon.processAudio,
    
    // Constants for reference from JS side if needed
    CONSTANTS: {
        SAMPLE_RATE: 48000
    }
};
