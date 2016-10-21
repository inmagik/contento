import React, { Component } from 'react'
import Region from './Region'

export default class ContentEditor extends Component {
  constructor(props) {
    super(props)
    this.state = {
      regions: props.regions,
    }
    this.updateFragment = this.updateFragment.bind(this)
    this.updateFragments = this.updateFragments.bind(this)
    this.removeFragment = this.removeFragment.bind(this)
    this.save= this.save.bind(this)
  }

  save() {
    this.props.saveRegions(this.state.regions)
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

  render() {
    const { regions } = this.state
    return (
      <div>
        {Object.keys(regions).map(name => (
          <Region
            key={name}
            name={name}
            fragments={regions[name]}
            updateFragment={(i, frag) => this.updateFragment(name, i, frag)}
            updateFragments={(frags) => this.updateFragments(name, frags)}
            removeFragment={(i) => this.removeFragment(name, i)}
          />
        ))}
      </div>
    )
  }
}
