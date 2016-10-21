// Store hooks
const hooks = {}

// Register to hook
const register = (key, bootstrapper, options = {}) => {
  hooks[key] = { bootstrapper, options }
}

// Unregister from hook
const unregister = (key) => {
  delete hooks[key]
}

// Boot hooks
const boot = () => {
  Array.from(document.querySelectorAll('[data-jshook]')).forEach(element => {
    const key = element.getAttribute('data-jshook')

    if (typeof hooks[key] === 'undefined') {
      console.warn(`No hook defined for key ${key}`)
      return
    }

    // Go!
    // TODO: User options... { options }
    const { bootstrapper } = hooks[key]
    bootstrapper(element)
  })
}

// JsHook
export default { register, unregister, boot }
