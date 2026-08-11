export function ScrollIndicator({ hidden }: { hidden: boolean }) {
  return (
    <a className={`scroll-indicator ${hidden ? 'is-hidden' : ''}`} href="#deploy" aria-label="Faire défiler vers la scène suivante">
      <span>SCROLL</span><i aria-hidden="true" />
    </a>
  )
}
