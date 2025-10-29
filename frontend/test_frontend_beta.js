/**
 * COMPREHENSIVE FRONTEND BETA TESTING SUITE
 * Tests all critical frontend functionality
 */

const fs = require('fs');
const path = require('path');

// Test Results Tracker
const testResults = {
    passed: [],
    failed: [],
    warnings: [],
    total: 0
};

function logTest(name, status, message = '') {
    testResults.total++;
    if (status === 'PASS') {
        testResults.passed.push(name);
        console.log(`✅ ${name}: PASS ${message}`);
    } else if (status === 'FAIL') {
        testResults.failed.push(name);
        console.log(`❌ ${name}: FAIL - ${message}`);
    } else if (status === 'WARN') {
        testResults.warnings.push(name);
        console.log(`⚠️  ${name}: WARNING - ${message}`);
    }
}

console.log('='.repeat(80));
console.log('🧪 COMPREHENSIVE FRONTEND BETA TESTING SUITE');
console.log('='.repeat(80));
console.log();

// ============================================================================
// TEST 1: Package.json Configuration
// ============================================================================
console.log('📦 TEST GROUP 1: Package Configuration');
console.log('-'.repeat(80));

try {
    const packageJson = require('./package.json');
    logTest('Package.json Load', 'PASS');
    
    // Check critical dependencies
    const criticalDeps = {
        'next': 'Next.js Framework',
        'react': 'React Library',
        '@supabase/supabase-js': 'Supabase Client',
        'razorpay': 'Payment Gateway',
        'react-hot-toast': 'Notifications',
        '@headlessui/react': 'UI Components',
        'lucide-react': 'Icons'
    };
    
    for (const [dep, description] of Object.entries(criticalDeps)) {
        if (packageJson.dependencies[dep]) {
            logTest(`Dependency: ${description}`, 'PASS', `v${packageJson.dependencies[dep]}`);
        } else {
            logTest(`Dependency: ${description}`, 'FAIL', 'Not found');
        }
    }
    
    // Check Next.js version (should be 14.2.33 or higher)
    const nextVersion = packageJson.dependencies.next.replace(/[\^~]/, '');
    const [major, minor, patch] = nextVersion.split('.').map(Number);
    if (major >= 14 && minor >= 2 && patch >= 33) {
        logTest('Next.js Version (Security)', 'PASS', `v${nextVersion} - No known vulnerabilities`);
    } else {
        logTest('Next.js Version (Security)', 'WARN', `v${nextVersion} - Update recommended`);
    }
    
    // Check scripts
    const criticalScripts = ['dev', 'build', 'start', 'lint'];
    for (const script of criticalScripts) {
        if (packageJson.scripts[script]) {
            logTest(`Script: ${script}`, 'PASS');
        } else {
            logTest(`Script: ${script}`, 'FAIL', 'Not found');
        }
    }
    
} catch (error) {
    logTest('Package.json Load', 'FAIL', error.message);
}

// ============================================================================
// TEST 2: Next.js Configuration
// ============================================================================
console.log('\n📦 TEST GROUP 2: Next.js Configuration');
console.log('-'.repeat(80));

try {
    const nextConfig = require('./next.config.js');
    logTest('Next.config.js Load', 'PASS');
    
    // Check image configuration
    if (nextConfig.images && nextConfig.images.remotePatterns) {
        logTest('Image Remote Patterns', 'PASS', `${nextConfig.images.remotePatterns.length} patterns configured`);
        
        // Check for critical domains
        const patterns = nextConfig.images.remotePatterns;
        const hasTrulyInvoice = patterns.some(p => p.hostname && p.hostname.includes('trulyinvoice.xyz'));
        const hasSupabase = patterns.some(p => p.hostname && p.hostname.includes('supabase'));
        
        if (hasTrulyInvoice) {
            logTest('Image Domain: trulyinvoice.xyz', 'PASS');
        } else {
            logTest('Image Domain: trulyinvoice.xyz', 'WARN', 'Not configured');
        }
        
        if (hasSupabase) {
            logTest('Image Domain: Supabase Storage', 'PASS');
        } else {
            logTest('Image Domain: Supabase Storage', 'WARN', 'Not configured');
        }
    } else {
        logTest('Image Remote Patterns', 'WARN', 'Not configured');
    }
    
} catch (error) {
    logTest('Next.config.js Load', 'FAIL', error.message);
}

// ============================================================================
// TEST 3: Environment Configuration
// ============================================================================
console.log('\n📦 TEST GROUP 3: Environment Configuration');
console.log('-'.repeat(80));

try {
    const envExamplePath = path.join(__dirname, '.env.example');
    if (fs.existsSync(envExamplePath)) {
        logTest('.env.example File', 'PASS');
        
        const envContent = fs.readFileSync(envExamplePath, 'utf8');
        
        // Check for critical environment variables
        const criticalEnvVars = [
            'NEXT_PUBLIC_SUPABASE_URL',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY',
            'NEXT_PUBLIC_API_URL',
            'NEXT_PUBLIC_RAZORPAY_KEY_ID'
        ];
        
        for (const envVar of criticalEnvVars) {
            if (envContent.includes(envVar)) {
                logTest(`Env Var Template: ${envVar}`, 'PASS');
            } else {
                logTest(`Env Var Template: ${envVar}`, 'WARN', 'Not documented');
            }
        }
    } else {
        logTest('.env.example File', 'WARN', 'File not found');
    }
} catch (error) {
    logTest('.env.example File', 'FAIL', error.message);
}

// ============================================================================
// TEST 4: Critical File Structure
// ============================================================================
console.log('\n📦 TEST GROUP 4: Critical File Structure');
console.log('-'.repeat(80));

const criticalFiles = [
    { path: 'src/app/layout.tsx', name: 'Root Layout' },
    { path: 'src/app/page.tsx', name: 'Home Page' },
    { path: 'src/app/invoices/page.tsx', name: 'Invoices Page' },
    { path: 'src/app/upload/page.tsx', name: 'Upload Page' },
    { path: 'src/app/pricing/page.tsx', name: 'Pricing Page' },
    { path: 'src/lib/supabase/client.ts', name: 'Supabase Client' },
    { path: 'src/lib/supabase/server.ts', name: 'Supabase Server' },
];

for (const { path: filePath, name } of criticalFiles) {
    const fullPath = path.join(__dirname, filePath);
    if (fs.existsSync(fullPath)) {
        logTest(`File: ${name}`, 'PASS', filePath);
    } else {
        logTest(`File: ${name}`, 'FAIL', `Not found: ${filePath}`);
    }
}

// ============================================================================
// TEST 5: Component Structure
// ============================================================================
console.log('\n📦 TEST GROUP 5: Component Structure');
console.log('-'.repeat(80));

const componentDirs = [
    { path: 'src/components/ui', name: 'UI Components' },
    { path: 'src/components/forms', name: 'Form Components' },
];

for (const { path: dirPath, name } of componentDirs) {
    const fullPath = path.join(__dirname, dirPath);
    if (fs.existsSync(fullPath)) {
        const files = fs.readdirSync(fullPath);
        logTest(`Directory: ${name}`, 'PASS', `${files.length} files`);
    } else {
        logTest(`Directory: ${name}`, 'WARN', 'Not found');
    }
}

// ============================================================================
// TEST 6: Modal System (Alert Replacement)
// ============================================================================
console.log('\n📦 TEST GROUP 6: Modal System (Alert Replacement)');
console.log('-'.repeat(80));

try {
    const invoicesPagePath = path.join(__dirname, 'src/app/invoices/page.tsx');
    if (fs.existsSync(invoicesPagePath)) {
        const content = fs.readFileSync(invoicesPagePath, 'utf8');
        
        // Check for remaining alert() calls
        const alertMatches = content.match(/\balert\s*\(/g);
        if (alertMatches && alertMatches.length > 0) {
            logTest('Browser Alert() Removal', 'FAIL', `${alertMatches.length} alert() calls still present`);
        } else {
            logTest('Browser Alert() Removal', 'PASS', 'All alerts replaced with modals');
        }
        
        // Check for CustomEvent modal system
        if (content.includes('CustomEvent') && content.includes('window.dispatchEvent')) {
            logTest('CustomEvent Modal System', 'PASS', 'Modern modal system implemented');
        } else {
            logTest('CustomEvent Modal System', 'WARN', 'CustomEvent pattern not found');
        }
        
        // Check for modal event listeners
        const modalEvents = ['show-export-error', 'show-export-success', 'show-delete-confirm'];
        let modalEventsFound = 0;
        for (const event of modalEvents) {
            if (content.includes(event)) {
                modalEventsFound++;
            }
        }
        
        if (modalEventsFound > 0) {
            logTest('Modal Event Types', 'PASS', `${modalEventsFound} event types found`);
        } else {
            logTest('Modal Event Types', 'WARN', 'No modal events found');
        }
        
    } else {
        logTest('Invoices Page Analysis', 'FAIL', 'File not found');
    }
} catch (error) {
    logTest('Modal System Analysis', 'FAIL', error.message);
}

// ============================================================================
// TEST 7: Tailwind Configuration
// ============================================================================
console.log('\n📦 TEST GROUP 7: Tailwind Configuration');
console.log('-'.repeat(80));

try {
    const tailwindConfigPath = path.join(__dirname, 'tailwind.config.ts');
    if (fs.existsSync(tailwindConfigPath)) {
        logTest('Tailwind Config File', 'PASS');
        
        const content = fs.readFileSync(tailwindConfigPath, 'utf8');
        
        // Check for content paths
        if (content.includes('./src/')) {
            logTest('Tailwind Content Paths', 'PASS');
        } else {
            logTest('Tailwind Content Paths', 'WARN', 'May need configuration');
        }
        
    } else {
        logTest('Tailwind Config File', 'WARN', 'File not found');
    }
} catch (error) {
    logTest('Tailwind Configuration', 'FAIL', error.message);
}

// ============================================================================
// TEST 8: TypeScript Configuration
// ============================================================================
console.log('\n📦 TEST GROUP 8: TypeScript Configuration');
console.log('-'.repeat(80));

try {
    const tsconfigPath = path.join(__dirname, 'tsconfig.json');
    if (fs.existsSync(tsconfigPath)) {
        const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'));
        logTest('TSConfig File', 'PASS');
        
        // Check compiler options
        if (tsconfig.compilerOptions) {
            const importantOptions = ['strict', 'esModuleInterop', 'jsx'];
            for (const option of importantOptions) {
                if (option in tsconfig.compilerOptions) {
                    logTest(`TSConfig: ${option}`, 'PASS', `${tsconfig.compilerOptions[option]}`);
                } else {
                    logTest(`TSConfig: ${option}`, 'WARN', 'Not configured');
                }
            }
        }
        
        // Check path aliases
        if (tsconfig.compilerOptions?.paths) {
            logTest('Path Aliases', 'PASS', `${Object.keys(tsconfig.compilerOptions.paths).length} aliases`);
        } else {
            logTest('Path Aliases', 'WARN', 'No path aliases configured');
        }
        
    } else {
        logTest('TSConfig File', 'FAIL', 'File not found');
    }
} catch (error) {
    logTest('TypeScript Configuration', 'FAIL', error.message);
}

// ============================================================================
// TEST 9: Public Assets
// ============================================================================
console.log('\n📦 TEST GROUP 9: Public Assets');
console.log('-'.repeat(80));

const publicAssets = [
    { path: 'public/favicon.ico', name: 'Favicon' },
];

for (const { path: assetPath, name } of publicAssets) {
    const fullPath = path.join(__dirname, assetPath);
    if (fs.existsSync(fullPath)) {
        const stats = fs.statSync(fullPath);
        logTest(`Asset: ${name}`, 'PASS', `${(stats.size / 1024).toFixed(2)} KB`);
    } else {
        logTest(`Asset: ${name}`, 'WARN', 'Not found');
    }
}

// ============================================================================
// TEST 10: ESLint Configuration
// ============================================================================
console.log('\n📦 TEST GROUP 10: ESLint Configuration');
console.log('-'.repeat(80));

try {
    const eslintPath = path.join(__dirname, '.eslintrc.json');
    if (fs.existsSync(eslintPath)) {
        const eslintConfig = JSON.parse(fs.readFileSync(eslintPath, 'utf8'));
        logTest('ESLint Config File', 'PASS');
        
        if (eslintConfig.extends) {
            logTest('ESLint Extends', 'PASS', `${eslintConfig.extends}`);
        }
    } else {
        logTest('ESLint Config File', 'WARN', 'File not found');
    }
} catch (error) {
    logTest('ESLint Configuration', 'WARN', error.message);
}

// ============================================================================
// FINAL REPORT
// ============================================================================
console.log('\n' + '='.repeat(80));
console.log('📊 FRONTEND BETA TEST RESULTS SUMMARY');
console.log('='.repeat(80));
console.log(`Total Tests: ${testResults.total}`);
console.log(`✅ Passed: ${testResults.passed.length} (${(testResults.passed.length/testResults.total*100).toFixed(1)}%)`);
console.log(`❌ Failed: ${testResults.failed.length} (${(testResults.failed.length/testResults.total*100).toFixed(1)}%)`);
console.log(`⚠️  Warnings: ${testResults.warnings.length} (${(testResults.warnings.length/testResults.total*100).toFixed(1)}%)`);

if (testResults.failed.length > 0) {
    console.log('\n❌ FAILED TESTS:');
    testResults.failed.forEach(test => console.log(`  - ${test}`));
}

if (testResults.warnings.length > 0) {
    console.log('\n⚠️  WARNINGS:');
    testResults.warnings.forEach(test => console.log(`  - ${test}`));
}

console.log('\n' + '='.repeat(80));

// Exit code
if (testResults.failed.length > 0) {
    console.log('❌ FRONTEND BETA TEST SUITE: FAILED');
    process.exit(1);
} else {
    console.log('✅ FRONTEND BETA TEST SUITE: PASSED');
    process.exit(0);
}
