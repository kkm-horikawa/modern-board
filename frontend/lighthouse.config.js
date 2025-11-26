/**
 * Lighthouse Configuration
 *
 * This configuration file defines settings for running Lighthouse performance,
 * accessibility, best practices, and SEO tests.
 */

module.exports = {
  extends: 'lighthouse:default',

  settings: {
    // Run in headless mode for CI/CD environments
    onlyCategories: [
      'performance',
      'accessibility',
      'best-practices',
      'seo'
    ],

    // Chrome flags for headless execution
    chromeFlags: [
      '--headless',
      '--disable-gpu',
      '--no-sandbox',
      '--disable-dev-shm-usage'
    ],

    // Output configuration
    output: ['html', 'json'],

    // Throttling settings (default mobile)
    throttling: {
      rttMs: 40,
      throughputKbps: 10 * 1024,
      cpuSlowdownMultiplier: 1,
      requestLatencyMs: 0,
      downloadThroughputKbps: 0,
      uploadThroughputKbps: 0
    },

    // Screen emulation (mobile)
    screenEmulation: {
      mobile: true,
      width: 375,
      height: 667,
      deviceScaleFactor: 2,
      disabled: false
    },

    // Form factor
    formFactor: 'mobile',

    // Skip certain audits that may not be relevant
    skipAudits: []
  },

  // CI-specific settings
  ci: {
    collect: {
      numberOfRuns: 3,
      settings: {
        chromeFlags: '--no-sandbox --disable-gpu'
      }
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
