- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-the-app-runs-on-my-laptop.md`
  summary: Configure htmx 2 so 4xx error fragments are swapped in (or handled per UX-DR-71/72: inline "Couldn't send. Try again." and reload on 409), when the first HTMX action is built (Story 2.3).
  evidence: htmx 2.x does not swap 4xx/5xx responses by default and `app/templates/base.html` sets no `htmx.config.responseHandling`; unreachable in Story 1.1 because no HTMX action exists yet (severity medium, unverified).
