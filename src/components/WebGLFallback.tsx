export function WebGLFallback() {
  return (
    <div className="webgl-fallback" aria-hidden="true">
      <div className="fallback-core" />
      <span className="fallback-orbit fallback-orbit--one" />
      <span className="fallback-orbit fallback-orbit--two" />
    </div>
  )
}
