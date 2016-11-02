import React, { Component } from 'react'
import Region from './Region'

export default class ContentEditor extends Component {
  constructor(props) {
    super(props)
    this.state = {
      regions: props.regions,
    }
    this.updateFragment = this.updateFragment.bind(this)
    this.updateFragmentData = this.updateFragmentData.bind(this)
    this.updateFragments = this.updateFragments.bind(this)
    this.removeFragment = this.removeFragment.bind(this)
    this.addFragment = this.addFragment.bind(this)
    this.save = this.save.bind(this)
  }

  save() {
    this.props.save(this.state.regions)
  }

  updateFragment(name, fragmentIndex, newFragment) {
    const { regions } = this.state;
    this.setState({
      regions: {
        ...regions,
        [name]: regions[name].map((fragment, index) => (
          index === fragmentIndex ? newFragment : fragment
        ))
      }
    }, this.save)
  }

  updateFragmentData(name, fragmentIndex, data) {
    const { regions } = this.state;
    this.setState({
      regions: {
        ...regions,
        [name]: regions[name].map((fragment, index) => (
          index === fragmentIndex ? { ...fragment, data } : fragment
        ))
      }
    }, this.save)
  }

  updateFragments(name, newFragments) {
    const { regions } = this.state
    this.setState({
      regions: {
        ...regions,
        [name]: newFragments.map(fragment => fragment) // Make a new array instance
      }
    }, this.save)
  }

  removeFragment(name, fragmentIndex) {
    const { regions } = this.state
    this.setState({
      regions: {
        ...regions,
        [name]: [
          ...regions[name].slice(0, fragmentIndex),
          ...regions[name].slice(fragmentIndex + 1)
        ]
      }
    }, this.save)
  }

  addFragment(name, fragment) {
    const { regions } = this.state
    this.setState({
      regions: {
        ...regions,
        [name]: [fragment, ...regions[name]]
      }
    }, this.save)
  }

  render() {
    const { regions } = this.state
    const { fragmentsSchemas } = this.props

    return (
      <div>
        {Object.keys(regions).map(name => (
          <Region
            key={name}
            name={name}
            fragments={regions[name]}
            fragmentsSchemas={fragmentsSchemas}
            updateFragments={(frags) => this.updateFragments(name, frags)}
            updateFragment={(i, frag) => this.updateFragment(name, i, frag)}
            updateFragmentData={(i, data) => this.updateFragmentData(name, i, data)}
            removeFragment={(i) => this.removeFragment(name, i)}
            addFragment={(frag) => this.addFragment(name, frag)}
          />
        ))}
      </div>
    )
  }
}
