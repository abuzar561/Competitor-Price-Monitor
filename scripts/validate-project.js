const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const failures = [];

const requiredFiles = [
  "README.md",
  "LICENSE",
  "CHANGELOG.md",
  "CONTRIBUTING.md",
  "SECURITY.md",
  ".env.example",
  ".gitignore",
  ".editorconfig",
  ".gitattributes",
  "requirements.txt",
  "src/price_monitor.py",
  "workflow/competitor-price-monitor.json",
  "workflow/README.md",
  "docs/SETUP.md",
  "docs/WORKFLOW.md",
  "docs/PAYLOAD.md",
  "docs/TROUBLESHOOTING.md",
  "examples/payload.example.json",
  ".github/workflows/validate.yml"
];

function fail(message) {
  failures.push(message);
}

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function listFiles(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);

    if (entry.name === ".git" || entry.name === "node_modules" || entry.name === ".venv") {
      return [];
    }

    if (entry.isDirectory()) {
      return listFiles(fullPath);
    }

    return [fullPath];
  });
}

function isTextFile(filePath) {
  const textBasenames = new Set([
    ".editorconfig",
    ".env.example",
    ".gitattributes",
    ".gitignore",
    "LICENSE"
  ]);

  return [
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml"
  ].includes(path.extname(filePath)) || textBasenames.has(path.basename(filePath));
}

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(root, file))) {
    fail(`Missing required file: ${file}`);
  }
}

const workflowPath = path.join(root, "workflow/competitor-price-monitor.json");
let workflow;

try {
  workflow = JSON.parse(fs.readFileSync(workflowPath, "utf8"));
} catch (error) {
  fail(`Workflow JSON is invalid: ${error.message}`);
}

if (workflow) {
  const nodeNames = new Set((workflow.nodes || []).map((node) => node.name));
  const requiredNodes = [
    "Price Update Webhook",
    "Log Price Snapshot",
    "Price Below Target?",
    "Send Price Drop Alert",
    "Send Status Email"
  ];

  for (const nodeName of requiredNodes) {
    if (!nodeNames.has(nodeName)) {
      fail(`Workflow missing node: ${nodeName}`);
    }
  }

  if (workflow.name !== "Competitor Price Monitor") {
    fail("Workflow name should be 'Competitor Price Monitor'.");
  }

  if (workflow.active !== false) {
    fail("Workflow export should be inactive for safe import.");
  }

  if (workflow.id || workflow.versionId || workflow.tags) {
    fail("Workflow should not include root export identifiers.");
  }

  if (workflow.meta && workflow.meta.instanceId) {
    fail("Workflow should not include n8n instance metadata.");
  }

  if (!workflow.meta || workflow.meta.templateCredsSetupCompleted !== false) {
    fail("Workflow should require users to configure credentials after import.");
  }

  const workflowText = JSON.stringify(workflow);

  if (/"credentials"\s*:/.test(workflowText)) {
    fail("Workflow should not include exported credential bindings.");
  }

  if (/"webhookId"\s*:/.test(workflowText)) {
    fail("Workflow should not include exported webhook IDs.");
  }

  const columns =
    workflow.nodes.find((node) => node.name === "Log Price Snapshot")?.parameters?.columns?.value || {};

  for (const column of ["Product Name", "Price", "Target Price", "Alert Type", "Currency", "Timestamp", "URL"]) {
    if (!Object.prototype.hasOwnProperty.call(columns, column)) {
      fail(`Workflow missing Google Sheets column mapping: ${column}`);
    }
  }

  for (const [sourceNode, outputs] of Object.entries(workflow.connections || {})) {
    if (!nodeNames.has(sourceNode)) {
      fail(`Workflow connection references missing source node: ${sourceNode}`);
    }

    for (const outputGroup of outputs.main || []) {
      for (const output of outputGroup) {
        if (!nodeNames.has(output.node)) {
          fail(`Workflow connection references missing target node: ${output.node}`);
        }
      }
    }
  }
}

const legacyAutomationRegex = new RegExp(
  ["insta" + "loader", "instagram" + "-spy", "mab" + "uzar"].join("|"),
  "i"
);

const forbiddenPatterns = [
  { label: "private n8n cloud URL", regex: /https?:\/\/[^"'\s]+\.app\.n8n\.cloud/i },
  { label: "private Google Sheet URL", regex: /docs\.google\.com\/spreadsheets\/d\/[A-Za-z0-9_-]{20,}/i },
  { label: "private Gmail address", regex: /[A-Z0-9._%+-]+@gmail\.com/i },
  { label: "legacy social automation text", regex: legacyAutomationRegex },
  { label: "mojibake text", regex: /[\u00f0\u0178\u00e2\u0161\u00ef\u00b8]/ }
];

for (const filePath of listFiles(root).filter(isTextFile)) {
  const relativePath = path.relative(root, filePath).replace(/\\/g, "/");
  const content = fs.readFileSync(filePath, "utf8");

  for (const { label, regex } of forbiddenPatterns) {
    if (regex.test(content)) {
      fail(`${relativePath} contains ${label}.`);
    }
  }
}

const scraperSource = fs.existsSync(path.join(root, "src/price_monitor.py"))
  ? readText("src/price_monitor.py")
  : "";

for (const envName of ["PRODUCT_URL", "PRICE_SELECTOR", "TARGET_PRICE", "N8N_WEBHOOK_URL"]) {
  if (!scraperSource.includes(envName)) {
    fail(`Scraper should support ${envName}.`);
  }
}

try {
  const examplePayload = JSON.parse(readText("examples/payload.example.json"));
  for (const field of ["product_name", "price", "currency", "url", "target_price", "alert_type", "timestamp"]) {
    if (!Object.prototype.hasOwnProperty.call(examplePayload, field)) {
      fail(`Example payload missing field: ${field}`);
    }
  }
} catch (error) {
  fail(`Example payload JSON is invalid: ${error.message}`);
}

if (failures.length > 0) {
  console.error("Project validation failed:");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Project validation passed.");
