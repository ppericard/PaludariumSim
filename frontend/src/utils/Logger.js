const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
};

// Default level
let currentLevel = LOG_LEVELS.INFO;

const logs = [];
const MAX_LOGS = 100;

const addLog = (level, message, ...args) => {
    const timestamp = new Date().toISOString();
    const logEntry = { timestamp, level, message, args };
    logs.push(logEntry);
    if (logs.length > MAX_LOGS) {
        logs.shift();
    }
};

const Logger = {
    setLevel: (level) => {
        if (LOG_LEVELS[level] !== undefined) {
            currentLevel = LOG_LEVELS[level];
        }
    },

    getLogs: () => [...logs],

    debug: (message, ...args) => {
        addLog('DEBUG', message, ...args);
        if (currentLevel <= LOG_LEVELS.DEBUG) {
            console.debug(`%c[DEBUG] ${message}`, 'color: #7f8c8d', ...args);
        }
    },

    info: (message, ...args) => {
        addLog('INFO', message, ...args);
        if (currentLevel <= LOG_LEVELS.INFO) {
            console.log(`%c[INFO] ${message}`, 'color: #2980b9', ...args);
        }
    },

    warn: (message, ...args) => {
        addLog('WARN', message, ...args);
        if (currentLevel <= LOG_LEVELS.WARN) {
            console.warn(`%c[WARN] ${message}`, 'color: #f39c12', ...args);
        }
    },

    error: (message, ...args) => {
        addLog('ERROR', message, ...args);
        if (currentLevel <= LOG_LEVELS.ERROR) {
            console.error(`%c[ERROR] ${message}`, 'color: #c0392b', ...args);
        }
    }
};

export default Logger;
