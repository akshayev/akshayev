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
  🏅 HackerRank Software Engineer certificate &nbsp;·&nbsp; 🎓 Google 5-Day AI Agents Intensive
</p>

---

## 🏆 Selected work

<!--PROJECTS:START-->
<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/akshayev/ghost-data-deletion-audit-agent"><img src="assets/projects/ghost-data-deletion-audit-agent.svg" alt="Ghost Data Deletion-Audit Agent: Checks 518 data-deletion requests against messy evidence and reports what still exists. LLMs only handle narrow jobs, behind validation." width="100%"></a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/akshayev/citypulse-crm"><img src="assets/projects/citypulse-crm.svg" alt="CityPulse CRM: Lead-gen CRM on a Bronze, Silver, Gold pipeline with data-quality gates, a dead-letter queue, provider fallbacks and daily cost quotas." width="100%"></a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/akshayev/CityPulse-AI-Market-Intelligence-Agent"><img src="assets/projects/citypulse-market-intelligence-agent.svg" alt="CityPulse Market Intelligence Agent: Scrapes, cleans, stores and analyzes local-market data, then writes a report. The first version of the pipeline CityPulse CRM grew from." width="100%"></a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/akshayev/job-seeker-agent"><img src="assets/projects/job-seeker-agent.svg" alt="Job Seeker Agent: Reads a resume, finds matching jobs, scores each one and drafts a tailored cover letter. Capstone of the Google and Kaggle AI Agents course." width="100%"></a>
    </td>
  </tr>
</table>
<!--PROJECTS:END-->

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
