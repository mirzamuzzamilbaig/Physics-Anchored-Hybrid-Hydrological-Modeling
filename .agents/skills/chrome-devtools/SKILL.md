---
name: chrome-devtools
description: Control and inspect a live Chrome browser with Chrome DevTools MCP for reliable automation, in-depth debugging, network and console inspection, and performance/Lighthouse analysis.
---

# Chrome DevTools Live Automation & Inspection Skill

This skill guides the agent in orchestrating Google Chrome via the `chrome-devtools-mcp` server. It enables full access to the Chrome DevTools Protocol (CDP) for browser automation, web app debugging, network/console diagnostics, accessibility audits, and performance profiling.

## When to Use This Skill
- Controlling a live browser session (navigation, clicking, form submission, drag-and-drop, scrolling).
- Debugging web applications (inspecting console errors, network requests/responses, DOM trees).
- Taking DOM snapshots with semantic accessibility identifiers (`uid`).
- Capturing screenshots of full pages or individual UI components.
- Measuring web performance, recording timeline traces, and analyzing Core Web Vitals (LCP, CLS, INP).
- Running Lighthouse audits (Performance, Accessibility, Best Practices, SEO).
- Inspecting memory heap allocations and diagnosing leaks.
- Testing under emulated network constraints (throttling), CPU throttling, and mobile viewports.

---

## Tool Reference Map

All tools are invoked through `call_mcp_tool` with `ServerName: "chrome-devtools-mcp"` and `ToolName: "<tool_name>"`.

### 1. Browser Lifecycle & Navigation
| Tool | Arguments | Purpose |
| :--- | :--- | :--- |
| `list_pages` | `{}` | Lists all open Chrome tabs and identifies current active `pageId`. |
| `new_page` | `{"url": string}` | Opens a new tab (optional initial URL). |
| `select_page` | `{"pageId": number}` | Brings a specific tab to the foreground. |
| `close_page` | `{"pageId": number}` | Closes a tab. |
| `navigate_page` | `{"pageId": number, "type": "url"|"back"|"forward"|"reload", "url"?: string, "timeout"?: number}` | Navigates or reloads a page. |
| `resize_page` | `{"pageId": number, "width": number, "height": number}` | Resizes browser viewport dimensions. |

### 2. Inspection & DOM Exploration
| Tool | Arguments | Purpose |
| :--- | :--- | :--- |
| `take_snapshot` | `{"pageId": number, "verbose"?: boolean, "filePath"?: string}` | Primary DOM inspection tool. Returns an accessibility tree with element `uid`s for reliable interaction. |
| `take_screenshot` | `{"pageId": number, "fullPage"?: boolean, "uid"?: string, "format"?: "png"|"jpeg"|"webp", "filePath"?: string}` | Captures visual screenshots of viewport, full page, or specific element `uid`. |
| `evaluate_script` | `{"pageId": number, "function": string, "args"?: string[], "waitForStableDom"?: boolean}` | Executes JavaScript functions in the page context. Return values must be JSON-serializable. |

### 3. User Interactions
| Tool | Arguments | Purpose |
| :--- | :--- | :--- |
| `click` | `{"pageId": number, "uid": string, "button"?: "left"|"right"|"middle", "clickCount"?: number}` | Clicks element by `uid`. |
| `hover` | `{"pageId": number, "uid": string}` | Moves mouse over element by `uid`. |
| `fill` | `{"pageId": number, "uid": string, "value": string}` | Clears and sets value of input/textarea/select element. |
| `fill_form` | `{"pageId": number, "elements": [{"uid": string, "value": string}]}` | Fills multiple form elements in one atomic operation. |
| `type_text` | `{"pageId": number, "text": string, "delay"?: number}` | Types characters into focused element. |
| `press_key` | `{"pageId": number, "key": string}` | Dispatches keyboard key (e.g. `Enter`, `Tab`, `Escape`, `ArrowDown`). |
| `drag` | `{"pageId": number, "fromUid": string, "toUid": string}` | Performs drag-and-drop between elements. |
| `upload_file` | `{"pageId": number, "uid": string, "filePath": string}` | Attaches local file to file input element. |
| `wait_for` | `{"pageId": number, "selector"?: string, "text"?: string, "timeout"?: number}` | Waits for element appearance or DOM stabilization. |
| `handle_dialog` | `{"pageId": number, "action": "accept"|"dismiss", "promptText"?: string}` | Responds to native alert/confirm/prompt modals. |

### 4. Logging & Network Inspection
| Tool | Arguments | Purpose |
| :--- | :--- | :--- |
| `list_console_messages` | `{"pageId": number, "types"?: string[], "limit"?: number}` | Fetches browser console logs, warnings, errors, and uncaught exceptions. |
| `get_console_message` | `{"pageId": number, "messageId": number}` | Retrieves full stack trace and argument details for a specific log item. |
| `list_network_requests` | `{"pageId": number, "resourceTypes"?: string[], "limit"?: number}` | Lists intercepted HTTP requests with method, URL, status code, and timing. |
| `get_network_request` | `{"pageId": number, "requestId": string}` | Retrieves detailed headers, payload, and response body for a specific request. |

### 5. Performance, Memory & Diagnostics
| Tool | Arguments | Purpose |
| :--- | :--- | :--- |
| `performance_start_trace` | `{"pageId": number, "reload"?: boolean, "screenshots"?: boolean}` | Begins DevTools performance trace recording. |
| `performance_stop_trace` | `{"pageId": number, "filePath"?: string}` | Ends performance trace recording and compiles profile. |
| `performance_analyze_insight` | `{"pageId": number, "insight": string}` | Analyzes trace data for Core Web Vitals (LCP, CLS, INP) bottlenecks. |
| `lighthouse_audit` | `{"pageId": number, "categories"?: string[], "filePath"?: string}` | Executes automated Lighthouse audit. |
| `take_heapsnapshot` | `{"pageId": number, "filePath"?: string}` | Dumps V8 memory heap snapshot for memory leak analysis. |
| `emulate` | `{"pageId": number, "device"?: string, "networkThrottling"?: string, "cpuThrottling"?: number, "colorScheme"?: "dark"|"light"}` | Emulates device configurations, throttling, and appearance. |

---

## Standard Operating Procedures

### Scenario A: Navigating and Inspecting an Application
1. **Discover Page ID**:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "list_pages"
   {}
   ```
2. **Navigate to URL**:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "navigate_page"
   { "pageId": 1, "type": "url", "url": "http://localhost:3000" }
   ```
3. **Capture Semantic Snapshot**:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "take_snapshot"
   { "pageId": 1 }
   ```
   *Note: Note the `uid` values assigned to interactive elements for subsequent actions.*

### Scenario B: Form Automation and Interaction
1. Use `take_snapshot` to extract element `uid`s for inputs and buttons.
2. Fill input fields using `fill` or `fill_form`:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "fill"
   { "pageId": 1, "uid": "uid_username_input", "value": "test_user" }
   ```
3. Submit by clicking button or sending `Enter`:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "click"
   { "pageId": 1, "uid": "uid_submit_button" }
   ```
4. Verify outcome by snapshot or script evaluation:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "evaluate_script"
   { "pageId": 1, "function": "() => document.location.pathname" }
   ```

### Scenario C: Diagnosing Frontend Bugs & API Failures
1. Inspect console for uncaught errors:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "list_console_messages"
   { "pageId": 1, "types": ["error", "warning"] }
   ```
2. Inspect network requests for HTTP 4xx/5xx failures:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "list_network_requests"
   { "pageId": 1 }
   ```
3. Inspect failing response payload:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "get_network_request"
   { "pageId": 1, "requestId": "req_123" }
   ```

### Scenario D: Performance Auditing & Core Web Vitals
1. Start trace with reload:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "performance_start_trace"
   { "pageId": 1, "reload": true, "screenshots": true }
   ```
2. Stop trace:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "performance_stop_trace"
   { "pageId": 1 }
   ```
3. Run comprehensive Lighthouse audit:
   ```json
   // ServerName: "chrome-devtools-mcp", ToolName: "lighthouse_audit"
   { "pageId": 1, "categories": ["performance", "accessibility", "best-practices", "seo"] }
   ```
