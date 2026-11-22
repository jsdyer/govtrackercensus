export default {
  "title": "Gov Tracker Census",
  "intro": "Who else does a government homepage contact? Compare observed requests, scripts and cookies across a fixed public website sample.",
  "eyebrow": "GOVERNMENT WEBSITES / NETWORK OBSERVATIONS",
  "accent": "#765039",
  "tint": "#f1e7df",
  "method": [
    "A fixed set of 15 federal, British Columbia and Nova Scotia homepages is visited in a fresh Chromium context, with no consent choices, login or other interaction. Robots restrictions and navigation failures remain explicit. This is a homepage sample, not a census of every government website.",
    "Third-party means a different registrable domain, including private suffixes. It does not establish different ownership. The documented service signatures identify contact with analytics or tag-delivery domains; they do not prove personal-data collection, unlawful tracking or consent compliance.",
    "Cookie values, request bodies and URL query values are not retained. The archive contains destination hosts, paths, parameter names, resource types, response statuses and cookie metadata. Geography, browser version, timing and consent defaults can affect results.",
    "The diary compares subsequent captures. Initial capture is a baseline. A failed scan cannot demonstrate that a technology was removed."
  ],
  "id": "govtrackercensus",
  "explorer-title": "Follow the record.",
  "cadence": "Weekly automated collection. Source dates and capture dates are shown separately.",
  "facets": [
    {
      "key": "jurisdiction",
      "label": "Jurisdiction"
    },
    {
      "key": "status",
      "label": "Scan result"
    }
  ],
  "columns": [
    {
      "key": "title",
      "label": "Institution"
    },
    {
      "key": "jurisdiction",
      "label": "Jurisdiction"
    },
    {
      "key": "status",
      "label": "Scan result"
    },
    {
      "key": "third_party_count",
      "label": "Other domains"
    },
    {
      "key": "services",
      "label": "Known service signatures"
    },
    {
      "key": "cookie_count",
      "label": "Cookies"
    }
  ],
  "related": [
    {
      "label": "Tracker X-Ray",
      "url": "https://coolcode.ca/trackerxray/"
    },
    {
      "label": "GC Subdomain Watch",
      "url": "https://coolcode.ca/gc-subdomain-watch/"
    }
  ]
};
