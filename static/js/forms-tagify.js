/**
 * Tagify
 */

'use strict';

(async function () {
  // Basic
  //------------------------------------------------------
  const tagifyBasicEl = document.querySelector('#TagifyBasic');
  const TagifyBasic = new Tagify(tagifyBasicEl);

  // Custom list & inline suggestion
  //------------------------------------------------------
  const TagifyPerFeatureNameEl = document.querySelector('#TagifyPerFeatureName');
  const TagifyEngFeatureNameEl = document.querySelector('#TagifyEngFeatureName');

  let response = await fetch('/fetch/get-features/')
  let data = await response.json()
  const perFeatureNameList = data['per_feature_names']
  const engFeatureNameList = data['eng_feature_names']

  // Inline
  let TagifyPerFeatureName = new Tagify(TagifyPerFeatureNameEl, {
    whitelist: perFeatureNameList,
    maxTags: 1,
    dropdown: {
      maxItems: 100,
      classname: 'tags-inline',
      enabled: 0,
      closeOnSelect: false
    }
  });

  // Inline
  let TagifyEngFeatureName = new Tagify(TagifyEngFeatureNameEl, {
    whitelist: engFeatureNameList,
    maxTags: 1,
    dropdown: {
      maxItems: 100,
      classname: 'tags-inline',
      enabled: 0,
      closeOnSelect: false
    }
  });

  TagifyPerFeatureName.on('add', async function (e) {
    let featureName = e.detail.data.value
    let productId = document.querySelector('input[name="product"]:checked').value

    let response = await fetch(`/fetch/get-feature-details/?featureName=${featureName}&productId=${productId}`)
    let data = await response.json()

    document.querySelector('input[name="priority"]').value = data['priority']
    document.querySelector('input[name="engName"]').value = data['engFeatureName']
  })

})();
