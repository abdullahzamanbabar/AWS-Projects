import React, { Component } from 'react';
import paginate from 'paginate-array';

class AllUrls extends Component {
  constructor(props) {
    super(props);

    this.state = {
      posts: [],
      size: 3,
      page: 1,
      currPage: null
    }

    this.previousPage = this.previousPage.bind(this);
    this.nextPage = this.nextPage.bind(this);
  }

  clickHandler1 = () => {
    fetch(`https://l2qs966u0c.execute-api.us-east-2.amazonaws.com/prod/urls`)
      .then(response => response.json())
      .then(posts => {
        const { page, size } = this.state;

        const currPage = paginate(posts, page, size);

        this.setState({
          ...this.state,
          posts,
          currPage
        });
      });
  }

  previousPage() {
    const { currPage, page, size, posts } = this.state;

    if (page > 1) {
      const newPage = page - 1;
      const newCurrPage = paginate(posts, newPage, size);

      this.setState({
        ...this.state,
        page: newPage,
        currPage: newCurrPage
      });
    }
  }

  nextPage() {
    const { currPage, page, size, posts } = this.state;

    if (page < currPage.totalPages) {
      const newPage = page + 1;
      const newCurrPage = paginate(posts, newPage, size);
      this.setState({ ...this.state, page: newPage, currPage: newCurrPage });
    }
  }

  render() {
    const { page, size, currPage } = this.state;

    return (
      <div>
        <button onClick={this.clickHandler1}>GET URLs</button>
        <div>page: {page}</div>
        <div>size: {size}</div>
        {currPage &&
          <ol>
            {currPage.data.map(post => <li style={{padding: "10px"}}><a href={"https://"+post.URL_ADDRESS}>{post.URL_ADDRESS}</a></li>)}
          </ol>
        }
        <button onClick={this.previousPage}>Previous Page</button>
        <button onClick={this.nextPage}>Next Page</button>
      </div>
    )
  }
}

export default AllUrls;