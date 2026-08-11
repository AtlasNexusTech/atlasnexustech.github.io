# Framer Motion UI

> Production-grade animated React interfaces. Purposeful motion design for modern web apps.

[![Demo](https://img.shields.io/badge/demo-live-blue)](https://atlasnexusops.github.io/framer-motion-ui/)
[![Skill](https://img.shields.io/badge/skill-docs-green)](./SKILL.md)

## What is this?

A comprehensive skill and demo repository for creating **animated React pages and components** using [Framer Motion](https://www.framer.com/motion/). Use this as a reference whenever you need:

- Animated landing pages
- Page transitions
- Scroll-triggered reveals
- Interactive hover/tap effects
- Staggered list animations
- Parallax scrolling
- Gesture-based interactions
- Number counters
- Mount/unmount transitions

## Quick Start

```bash
npm install framer-motion
```

```jsx
import { motion, AnimatePresence } from "framer-motion";

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Hello World
</motion.div>
```

## Demo

Open [demo.html](./demo.html) in your browser to see all patterns in action, or visit the [live demo](https://atlasnexusops.github.io/framer-motion-ui/).

## Skill Documentation

See [SKILL.md](./SKILL.md) for the complete reference covering:
- Core primitives (`motion.div`, variants, `AnimatePresence`)
- Animation patterns (entrance, scroll, parallax, drag, counter)
- Easing reference
- Performance rules
- Accessibility (`useReducedMotion`)
- Delivery checklist

## Philosophy

Animation should:
1. **Guide attention** — lead the eye to what matters
2. **Communicate state** — loading, success, error, transition
3. **Create continuity** — make navigation feel spatial
4. **Delight without distracting** — subtle > excessive
