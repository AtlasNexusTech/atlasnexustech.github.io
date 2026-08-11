# Framer Motion UI Skill

Production-grade animated React interfaces using [Framer Motion](https://www.framer.com/motion/). Purposeful, performant animation that enhances UX — not decoration for its own sake.

## Core Philosophy

Animation should:
- **Guide attention** — lead the eye to what matters
- **Communicate state** — loading, success, error, transition
- **Create continuity** — make navigation feel spatial and connected
- **Delight without distracting** — subtle > excessive

## Setup

```bash
npm install framer-motion
```

Import pattern:

```jsx
import { motion, AnimatePresence, useInView, useScroll, useTransform, useSpring, useReducedMotion } from "framer-motion";
```

## Core Primitives

### 1. `motion.div` — The Basic Building Block

Replace any HTML element with its `motion.*` equivalent:

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
>
  Content that fades in and slides up
</motion.div>
```

### 2. Variants — Orchestrated Animation

Coordinate parent/child animations with variants:

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } }
};

<motion.div variants={container} initial="hidden" animate="show">
  {items.map(item => (
    <motion.div key={item.id} variants={item}>{item.content}</motion.div>
  ))}
</motion.div>
```

### 3. `AnimatePresence` — Mount/Unmount Animations

Always wrap conditionally rendered elements:

```jsx
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

- `mode="wait"` — exit animation finishes before enter starts (page transitions)
- `mode="popLayout"` — removed elements pop out of layout immediately

## Animation Patterns

### Page Entrance

```jsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
>
  <h1>Welcome</h1>
</motion.div>
```

### Scroll-Triggered Reveal

```jsx
function RevealOnScroll({ children }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

### Parallax Scroll

```jsx
function ParallaxSection() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["-20%", "20%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0.6, 1, 0.6]);

  return (
    <motion.div ref={ref} style={{ y, opacity }}>
      Parallax content
    </motion.div>
  );
}
```

### Hover & Tap Interactions

```jsx
<motion.button
  whileHover={{ scale: 1.05, backgroundColor: "#2563eb" }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>
```

### Drag Interaction

```jsx
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 200 }}
  dragElastic={0.1}
  whileDrag={{ scale: 1.05, boxShadow: "0 20px 60px rgba(0,0,0,0.3)" }}
>
  Draggable card
</motion.div>
```

### Number Counter Animation

```jsx
function AnimatedCounter({ from = 0, to, duration = 2 }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  const count = useMotionValue(from);
  const rounded = useTransform(count, v => Math.round(v));

  useEffect(() => {
    if (isInView) {
      const controls = animate(count, to, { duration, ease: "easeOut" });
      return controls.stop;
    }
  }, [isInView]);

  return <motion.span ref={ref}>{rounded}</motion.span>;
}
```

### Layout Animation (auto-animate reflow)

```jsx
<motion.div layout className="grid grid-cols-3">
  {items.map(item => (
    <motion.div key={item.id} layout>{item.content}</motion.div>
  ))}
</motion.div>
```

## Easing Reference

| Easing | Use case |
|--------|----------|
| `"easeOut"` | Entrances — fast start, soft landing |
| `"easeIn"` | Exits — builds momentum out |
| `"easeInOut"` | Transitions between states |
| `[0.22, 1, 0.36, 1]` | Smooth, premium feel (custom bezier) |
| `{ type: "spring", stiffness: 300, damping: 25 }` | Bouncy, physical interactions |
| `{ type: "spring", stiffness: 100, damping: 30 }` | Soft, organic feel |

## Performance Rules

**Animate only transform + opacity** — they run on GPU, never trigger reflow:
- ✅ `x`, `y`, `scale`, `rotate`, `opacity`
- ❌ `width`, `height`, `top`, `left`, `margin` (use `layout` prop instead)

Use `will-change: transform` on heavily animated elements sparingly.

Always respect accessibility with `useReducedMotion()`:

```jsx
const prefersReduced = useReducedMotion();

<motion.div
  initial={prefersReduced ? {} : { opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
>
  Accessible content
</motion.div>
```

Avoid animating too many elements simultaneously — stagger them with `staggerChildren`.

## Full Example — Animated Landing Page Section

```jsx
const heroVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15, delayChildren: 0.3 }
  }
};

const childVariants = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } }
};

function HeroSection() {
  return (
    <motion.section
      variants={heroVariants}
      initial="hidden"
      animate="show"
      className="min-h-screen flex items-center justify-center"
    >
      <div className="text-center">
        <motion.h1 variants={childVariants} className="text-6xl font-bold">
          Build Something Beautiful
        </motion.h1>
        <motion.p variants={childVariants} className="text-xl text-gray-400 mt-4">
          Production-grade animation that means something
        </motion.p>
        <motion.div variants={childVariants} className="mt-8">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
            className="px-8 py-3 bg-blue-600 rounded-lg font-semibold"
          >
            Get Started
          </motion.button>
        </motion.div>
      </div>
    </motion.section>
  );
}
```

## Checklist Before Delivering

- [ ] `AnimatePresence` wraps every conditional render
- [ ] `exit` prop defined on every `motion.*` inside `AnimatePresence`
- [ ] Unique `key` props on animated list items
- [ ] Only animating transform/opacity properties (not layout props)
- [ ] `useReducedMotion()` respected for accessibility
- [ ] Spring physics used for interactive elements (drag, hover, tap)
- [ ] Stagger applied to lists of 3+ items
- [ ] No janky layout shifts (use `layout` prop for reflow animations)
