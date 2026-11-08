<p align="center">
  <img src="assets/header.svg" alt="Akshay EV: data engineering and AI agents. Python and SQL." width="100%">
</p>

<p align="center">
  <b>I build data pipelines and AI agents that check their own work.</b><br>
  Built with Claude Code, Codex and Antigravity, with tests and validation gates around everything they produce.
</p>

<p align="center">
  📍 Thrissur, Kerala, India &nbsp;·&nbsp; 🟢 Open to data engineering and AI agent roles: remote, hybrid, or on-site<br>
  📫 <a href="mailto:akshayev47@gmail.com">akshayev47@gmail.com</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/in/akshay-ev">LinkedIn</a>
</p>

<p align="center">
  <img src="assets/activity.svg" alt="Live activity: latest public commits and pull requests, and a 16-week contribution heatmap" width="100%">
</p>

<p align="center">
  <img src="assets/numbers.svg" alt="By the numbers: rank 28 of 4,094 in HackerRank Orchestrate; 375 tests; 100% deletion-status accuracy; 518 requests audited" width="100%">
</p>

<p align="center">
  🏅 HackerRank Software Engineer certificate &nbsp;·&nbsp; 🎓 Google 5-Day AI Agents Intensive
</p>

---

## 🏆 Selected work

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🏅 <a href="https://github.com/akshayev/ghost-data-deletion-audit-agent">Ghost Data Deletion-Audit Agent</a></h3>
      Checks 518 data-deletion requests against messy evidence (SQL, logs, PDFs, screenshots) and reports what still exists. <b>Rank 28 of 4,094</b> in HackerRank Orchestrate. A deterministic core does the work; LLMs only handle narrow jobs behind validation.<br><br>
      <sub><code>Python</code> · <code>pytest</code> · <code>LLM validation gates</code></sub>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ <a href="https://github.com/akshayev/citypulse-crm">CityPulse CRM</a></h3>
      Lead-gen CRM on a Bronze → Silver → Gold pipeline: Pydantic quality gates, dead-letter queue with backoff, provider fallbacks, daily cost quotas and LLM lead scoring.<br><br>
      <sub><code>Python</code> · <code>SQL</code> · <code>Supabase</code> · <code>Gemini</code></sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🏙️ <a href="https://github.com/akshayev/CityPulse-AI-Market-Intelligence-Agent">CityPulse Market Intelligence Agent</a></h3>
      Scrapes, cleans, stores and analyzes local-market data, then writes a report. The first version of the pipeline CityPulse CRM grew from.<br><br>
      <sub><code>Python</code> · <code>SQL</code> · <code>Supabase</code> · <code>Selenium</code></sub>
    </td>
    <td width="50%" valign="top">
      <h3>🕵️ <a href="https://github.com/akshayev/job-seeker-agent">Job Seeker Agent</a></h3>
      Reads a resume, finds matching jobs, scores each one and drafts a tailored cover letter. Capstone of the Google and Kaggle AI Agents course.<br><br>
      <sub><code>Python</code> · <code>Gemini</code> · <code>Streamlit</code></sub>
    </td>
  </tr>
</table>

### How the CityPulse pipeline flows

```mermaid
flowchart LR
    A["Scrape<br/>SerpApi, Selenium fallback"] --> B[("Bronze<br/>raw")]
    B --> C["Clean + compliance filter<br/>Pydantic contracts"]
    C --> D[("Silver<br/>cleaned")]
    D --> E["LLM heat score 0-100<br/>Gemini, Groq fallback"]
    E --> F[("Gold<br/>scored leads")]
    F --> G["Live Kanban board"]
    C -. "bad rows" .-> Q["Quarantine"]
    E -. "failed task" .-> R["Dead-letter queue<br/>retry with backoff"]
    R -.-> E
```

## 🤝 How I build

- **Tests first.** For the audit agent, expected outputs were written before the code that satisfies them. A golden-output lock catches silent changes.
- **Never trust a model blindly.** In the audit agent, only one of three models passed my validation gate, so only that one is used. Every model answer goes through code that can reject it.
- **Small, reviewable changes.** One concern per branch and per PR.
- **Secrets stay out of git.** A scan runs before anything is committed or pushed.

<details>
<summary><b>🎓 Experience, education and more projects</b></summary>

<br>

**Experience**
- Full Stack Developer Intern, Xpar (May – Oct 2026)
- Website Developer Intern, Strokx Technologies (May – Jun 2025)
- Programming Intern, Keltron (Apr – May 2024): Python scripting for data processing and validation
- Lead, CUCEK Photography Club (Apr 2026 – present; member since 2023)

**Education**
- B.Tech, Information Technology, Cochin University of Science and Technology (graduating 2027)

**Also built**
- [LeadFlow Pro](https://github.com/akshayev/LeadFlow-Pro): CRM with a Kanban board and live analytics
- [TravelSphere](https://github.com/akshayev/TravelSphere): travel-booking app with an admin dashboard

</details>
