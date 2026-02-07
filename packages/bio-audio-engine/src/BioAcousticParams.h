#ifndef BIO_ACOUSTIC_PARAMS_H
#define BIO_ACOUSTIC_PARAMS_H

namespace BioAcoustic {

    // Prime Directive: Biological Plausibility
    struct VocalConstraints {
        static constexpr double MIN_HUMAN_FUNDAMENTAL_FREQ = 85.0;  // Hz (Deep Bass)
        static constexpr double MAX_HUMAN_FUNDAMENTAL_FREQ = 1100.0; // Hz (Soprano High C)
        static constexpr double BREATH_THRESHOLD_MS = 250.0; // Minimum silence to trigger breath
    };

    // Prime Directive: Physics First
    struct AudioPhysics {
        static constexpr int SAMPLE_RATE = 48000; // DVD Quality / Standard for Video
        static constexpr int BIT_DEPTH = 24;      // Studio Quality
        static constexpr double SPEED_OF_SOUND = 343.0; // m/s at 20C
    };

    struct QuantizationRules {
        static constexpr double GHOST_NOTE_THRESHOLD_MS = 10.0; // Notes shorter than this are errors
    };
}

#endif // BIO_ACOUSTIC_PARAMS_H
