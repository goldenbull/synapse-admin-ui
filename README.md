# synapse-admin-ui
web ui for matrix-synapse administration

# structure
vue/axios --> vite dev server with a local proxy table --> synapse http api

note: axios have CORS problem when accessing synapse server,
use a vite dev server local proxy to bypass the issue.
see https://gist.github.com/brenopolanski/7f084f2ab8f817f6160deae1be629520

