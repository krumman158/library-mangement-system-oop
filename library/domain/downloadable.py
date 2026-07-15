class Downloadable:
 """Mixin: adds a capability, not an identity."""

 def download(self) -> str:
  return f"Downloading {self.title}..." # relies on the host class