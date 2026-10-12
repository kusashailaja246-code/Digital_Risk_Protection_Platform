import { useMemo, useState } from "react";
import "./App.css";

const initialApps = [
  {
    id: 1,
    name: "PayWave Rewards",
    developer: "PW Digital Services",
    store: "Google Play",
    category: "Finance",
    downloads: "10K+",
    risk: 96,
    status: "High Risk",
    reason: "Brand name similarity and unknown publisher",
    official: false,
  },
  {
    id: 2,
    name: "Pay Wave Official",
    developer: "PayWave Technologies",
    store: "Apple App Store",
    category: "Finance",
    downloads: "1M+",
    risk: 0,
    status: "Official",
    reason: "Verified official application",
    official: true,
  },
  {
    id: 3,
    name: "PayWave Support Help",
    developer: "Quick Support Apps",
    store: "Google Play",
    category: "Tools",
    downloads: "5K+",
    risk: 84,
    status: "High Risk",
    reason: "Added keywords and different developer",
    official: false,
  },
  {
    id: 4,
    name: "PayWave Wallet Pro",
    developer: "Smart Mobile Studio",
    store: "Apple App Store",
    category: "Finance",
    downloads: "2K+",
    risk: 72,
    status: "Medium Risk",
    reason: "Similar name; publisher is not recognized",
    official: false,
  },
  {
    id: 5,
    name: "PayWave Business",
    developer: "PayWave Technologies",
    store: "Google Play",
    category: "Business",
    downloads: "500K+",
    risk: 0,
    status: "Official",
    reason: "Verified official application",
    official: true,
  },
  {
    id: 6,
    name: "PayWav Rewards Center",
    developer: "Reward Hub Ltd",
    store: "Google Play",
    category: "Shopping",
    downloads: "1K+",
    risk: 89,
    status: "High Risk",
    reason: "Look-alike name and suspicious branding",
    official: false,
  },
];

function App() {
  const [brand, setBrand] = useState("PayWave");
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");
  const [apps, setApps] = useState(initialApps);
  const [selectedApp, setSelectedApp] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [notice, setNotice] = useState("");

  const filteredApps = useMemo(() => {
    return apps.filter((app) => {
      const text = `${app.name} ${app.developer} ${app.store}`.toLowerCase();
      const matchesSearch = text.includes(search.toLowerCase());
      const matchesFilter =
        filter === "All" ||
        (filter === "Suspicious" && !app.official) ||
        (filter === "Official" && app.official) ||
        (filter === "High Risk" && app.risk >= 80 && !app.official) ||
        (filter === "Medium Risk" &&
          app.risk >= 50 &&
          app.risk < 80 &&
          !app.official);

      return matchesSearch && matchesFilter;
    });
  }, [apps, search, filter]);

  const suspicious = apps.filter((app) => !app.official);
  const highRisk = suspicious.filter((app) => app.risk >= 80).length;
  const averageRisk = suspicious.length
    ? Math.round(
        suspicious.reduce((sum, app) => sum + app.risk, 0) /
          suspicious.length
      )
    : 0;

  function updateStatus(id, status) {
    setApps((current) =>
      current.map((app) =>
        app.id === id ? { ...app, status } : app
      )
    );
    setSelectedApp(null);
    setNotice(`Application marked as ${status}.`);
  }

  function saveProfile(event) {
    event.preventDefault();
    setShowProfile(false);
    setNotice(`Brand profile updated for ${brand}.`);
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-logo">
          <span className="logo-icon">◈</span>
          <div>
            <strong>Sentinel</strong>
            <small>Digital Risk Protection</small>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>
        <div className="workspace">
          <span className="workspace-avatar">P</span>
          <div>
            <strong>{brand} Inc.</strong>
            <small>Brand protection</small>
          </div>
          <span className="chevron">⌄</span>
        </div>

        <div className="nav-label">MONITORING</div>
        <nav className="navigation">
          <button className="nav-item" onClick={() => setFilter("All")}>
            <span>▦</span> Overview
          </button>
          <button
            className="nav-item"
            onClick={() => {
              setFilter("Suspicious");
              setNotice("");
            }}
          >
            <span>◎</span> Social Monitoring
          </button>
          <button className="nav-item active" onClick={() => setFilter("All")}>
            <span>▣</span> App Store Monitoring
            <span className="nav-count">{suspicious.length}</span>
          </button>
        </nav>

        <div className="nav-label">MANAGE</div>
        <nav className="navigation">
          <button className="nav-item" onClick={() => setShowProfile(true)}>
            <span>◇</span> Brand Profile
          </button>
          <button
            className="nav-item"
            onClick={() => setNotice("Reports are ready to be added in the next version.")}
          >
            <span>▤</span> Reports
          </button>
          <button
            className="nav-item"
            onClick={() => setNotice("Settings are ready to be added in the next version.")}
          >
            <span>⚙</span> Settings
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="protection-icon">✓</div>
          <strong>Protection active</strong>
          <p>Monitoring demo app inventory for potential brand impersonation.</p>
          <div className="sidebar-footer">SENTINEL PLATFORM · DEMO</div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumbs">
            <span>Monitoring</span><span>/</span><strong>App Store Monitoring</strong>
          </div>
          <div className="topbar-right">
            <span className="demo-pill"><i /> DEMO ENVIRONMENT</span>
            <button className="profile-button" onClick={() => setShowProfile(true)}>
              <span className="user-avatar">A</span>
              <span>Admin</span>
              <span>⌄</span>
            </button>
          </div>
        </header>

        <section className="page-content">
          <div className="page-heading">
            <div>
              <div className="eyebrow">EXTERNAL ATTACK SURFACE</div>
              <h1>App Store Monitoring</h1>
              <p className="subtitle">
                Discover suspicious mobile apps impersonating your brand.
              </p>
            </div>
            <button className="primary-button" onClick={() => setShowProfile(true)}>
              <span>＋</span> Configure brand
            </button>
          </div>

          {notice && (
            <div className="notice">
              <span>{notice}</span>
              <button onClick={() => setNotice("")}>✕</button>
            </div>
          )}

          <div className="monitor-status">
            <div className="status-symbol">✓</div>
            <div>
              <strong>Monitoring workspace ready</strong>
              <p>Demo inventory loaded · Official applications excluded from suspicious counts</p>
            </div>
            <span className="status-live"><i /> Demo active</span>
          </div>

          <div className="metrics-grid">
            <article className="metric-card">
              <div className="metric-top">
                <span>Apps discovered</span><span className="metric-icon blue">▣</span>
              </div>
              <div className="metric-value">{apps.length}</div>
              <div className="metric-foot">Across demo app stores</div>
            </article>
            <article className="metric-card">
              <div className="metric-top">
                <span>Potential impersonations</span><span className="metric-icon red">⚠</span>
              </div>
              <div className="metric-value">{suspicious.length}</div>
              <div className="metric-foot"><span className="red-text">Needs review</span> · Demo findings</div>
            </article>
            <article className="metric-card">
              <div className="metric-top">
                <span>High-risk apps</span><span className="metric-icon orange">↗</span>
              </div>
              <div className="metric-value">{highRisk}</div>
              <div className="metric-foot">Risk score ≥ 80</div>
            </article>
            <article className="metric-card">
              <div className="metric-top">
                <span>Average risk score</span><span className="metric-icon purple">◉</span>
              </div>
              <div className="metric-value">{averageRisk}<small>/100</small></div>
              <div className="risk-meter"><span style={{ width: `${averageRisk}%` }} /></div>
            </article>
          </div>

          <section className="inventory-panel">
            <div className="panel-heading">
              <div>
                <h2>Application inventory</h2>
                <p>Review detected apps and investigate potential brand misuse.</p>
              </div>
              <span className="inventory-count">{filteredApps.length} results</span>
            </div>

            <div className="inventory-toolbar">
              <div className="search-box">
                <span>⌕</span>
                <input
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="Search apps or developers..."
                  aria-label="Search apps or developers"
                />
                {search && <button onClick={() => setSearch("")}>✕</button>}
              </div>
              <select
                value={filter}
                onChange={(event) => setFilter(event.target.value)}
                aria-label="Filter applications"
              >
                <option>All</option>
                <option>Suspicious</option>
                <option>High Risk</option>
                <option>Medium Risk</option>
                <option>Official</option>
              </select>
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>APPLICATION</th>
                    <th>STORE</th>
                    <th>RISK SCORE</th>
                    <th>DETECTION</th>
                    <th>STATUS</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {filteredApps.map((app) => (
                    <tr key={app.id}>
                      <td>
                        <div className="app-name-cell">
                          <div className={`app-icon app-icon-${app.id % 4}`}>
                            {app.official ? "✓" : app.name.slice(0, 1)}
                          </div>
                          <div>
                            <strong>{app.name}</strong>
                            <small>{app.developer}</small>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className="store-name">
                          <span>{app.store === "Google Play" ? "▶" : "●"}</span>
                          {app.store}
                        </span>
                        <small className="download-text">{app.downloads} downloads</small>
                      </td>
                      <td>
                        {app.official ? (
                          <span className="score-official">—</span>
                        ) : (
                          <div className="score-cell">
                            <strong>{app.risk}</strong>
                            <div className="mini-meter">
                              <span
                                className={app.risk >= 80 ? "meter-high" : "meter-medium"}
                                style={{ width: `${app.risk}%` }}
                              />
                            </div>
                          </div>
                        )}
                      </td>
                      <td>
                        <div className="detection-reason">
                          <span className={app.official ? "reason-check" : "reason-alert"}>
                            {app.official ? "✓" : "!"}
                          </span>
                          <span>{app.reason}</span>
                        </div>
                      </td>
                      <td>
                        <span className={`status-badge ${
                          app.official ? "official" :
                          app.status === "Under Review" ? "review" :
                          app.risk >= 80 ? "high" : "medium"
                        }`}>
                          {app.status}
                        </span>
                      </td>
                      <td>
                        <button
                          className="details-button"
                          onClick={() => setSelectedApp(app)}
                          aria-label={`View details for ${app.name}`}
                        >
                          →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filteredApps.length === 0 && (
                <div className="empty-state">
                  <div>⌕</div>
                  <strong>No applications found</strong>
                  <p>Try another search term or change the filter.</p>
                  <button className="secondary-button" onClick={() => {
                    setSearch("");
                    setFilter("All");
                  }}>Clear filters</button>
                </div>
              )}
            </div>

            <div className="table-footer">
              <span>Showing {filteredApps.length} of {apps.length} demo applications</span>
              <span><i /> Official apps excluded from threat totals</span>
            </div>
          </section>

          <div className="bottom-grid">
            <section className="info-panel">
              <div className="info-icon">⌕</div>
              <div>
                <h3>Look-alike name detection</h3>
                <p>Demo findings consider similar names, added keywords, and unknown publishers.</p>
              </div>
              <span className="enabled-tag">Enabled</span>
            </section>
            <section className="info-panel">
              <div className="info-icon green-icon">✓</div>
              <div>
                <h3>Official asset exclusion</h3>
                <p>Apps marked official are excluded from suspicious app and risk calculations.</p>
              </div>
              <span className="enabled-tag">Enabled</span>
            </section>
          </div>

          <footer className="page-footer">
            Sentinel Digital Risk Protection <span>•</span> App Store Monitoring Prototype
            <span className="footer-note">Sample data only — not live threat intelligence</span>
          </footer>
        </section>
      </main>

      {showProfile && (
        <div className="modal-backdrop" onClick={() => setShowProfile(false)}>
          <section className="modal" onClick={(event) => event.stopPropagation()}>
            <div className="modal-heading">
              <div><div className="eyebrow">BRAND CONFIGURATION</div><h2>Brand profile</h2></div>
              <button onClick={() => setShowProfile(false)}>✕</button>
            </div>
            <p className="modal-description">
              Define your legitimate brand identity for app monitoring.
            </p>
            <form onSubmit={saveProfile}>
              <label>Company or brand name</label>
              <input value={brand} onChange={(event) => setBrand(event.target.value)} required />
              <label>Official publisher</label>
              <input defaultValue="PayWave Technologies" />
              <label>Official app stores</label>
              <div className="check-row"><span>✓</span> Google Play</div>
              <div className="check-row"><span>✓</span> Apple App Store</div>
              <div className="modal-note">
                This prototype uses sample assets and demo data. It does not connect to live app stores.
              </div>
              <div className="modal-actions">
                <button type="button" className="secondary-button" onClick={() => setShowProfile(false)}>Cancel</button>
                <button type="submit" className="primary-button">Save profile</button>
              </div>
            </form>
          </section>
        </div>
      )}

      {selectedApp && (
        <div className="modal-backdrop" onClick={() => setSelectedApp(null)}>
          <section className="modal detail-modal" onClick={(event) => event.stopPropagation()}>
            <div className="modal-heading">
              <div><div className="eyebrow">APPLICATION INVESTIGATION</div><h2>App details</h2></div>
              <button onClick={() => setSelectedApp(null)}>✕</button>
            </div>
            <div className="detail-app">
              <div className={`app-icon app-icon-${selectedApp.id % 4}`}>
                {selectedApp.official ? "✓" : selectedApp.name.slice(0, 1)}
              </div>
              <div><h3>{selectedApp.name}</h3><p>{selectedApp.developer}</p></div>
            </div>
            <div className="detail-row"><span>Store</span><strong>{selectedApp.store}</strong></div>
            <div className="detail-row"><span>Category</span><strong>{selectedApp.category}</strong></div>
            <div className="detail-row"><span>Downloads</span><strong>{selectedApp.downloads}</strong></div>
            <div className="detail-row"><span>Risk score</span><strong>{selectedApp.official ? "Official asset" : `${selectedApp.risk}/100`}</strong></div>
            <div className="detail-reason"><strong>Detection explanation</strong><p>{selectedApp.reason}</p></div>
            {selectedApp.official ? (
              <div className="modal-note">This is marked as an official asset and is excluded from threat totals.</div>
            ) : (
              <div className="modal-actions">
                <button className="secondary-button" onClick={() => updateStatus(selectedApp.id, "Under Review")}>Mark under review</button>
                <button className="primary-button" onClick={() => updateStatus(selectedApp.id, "Investigated")}>Mark investigated</button>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  );
}

export default App;