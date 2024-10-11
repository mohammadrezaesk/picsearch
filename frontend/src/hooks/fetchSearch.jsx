const fetchSearch = async ({ queryKey }) => {
  const { query, searchMode } = queryKey[1];

  const apiRes = await fetch(
    `http://localhost:8000/search?query=${query}&mode=${searchMode}`
  );
  if (!apiRes.ok) {
    throw new Error(
      `search/query=${query}&mode=${searchMode} fetch not ok.`
    );
  }
  return apiRes.json();
};

export default fetchSearch;
