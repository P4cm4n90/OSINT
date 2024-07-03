const EMAIL_FORMAT = '{first}.{last}@example.com'; // supported vars {first}{f}{last}{l}
/* ------ */

const people = [['Email','Position']];

const pplTotal = parseInt(document.querySelector('div.org-people__insights-container h2').textContent.trim().match(/([0-9,]+)\s/)[1].replace(/,/g,''));

// generate email from full name based on template
function generateEmail(fullName, template) {
  const cleanName = fullName.replace(/\-/,' ').replace(/[\']/g, '').trim(); // TODO this needs to bo tunned
  const nameParts = cleanName.split(/\s+/);
  const firstName = nameParts[0];
  const lastName = nameParts[nameParts.length - 1];

  const variables = {
    '{first}': firstName.toLowerCase(),
    '{f}': firstName[0].toLowerCase(),
    '{last}': lastName.toLowerCase(),
    '{l}': lastName[0].toLowerCase(),
  };

  return template.replace(/{first}|{f}|{last}|{l}/g, function(match) {
    return variables[match];
  });
}

// get People and generate CSV
let getPeopleRunningLock = 0;
function getPeople() {
  getPeopleRunningLock = 1;
  const profiles = document.querySelectorAll('.org-people-profile-card');
  if (profiles.length === pplTotal || !document.querySelector('.scaffold-finite-scroll__load-button')) {
    console.log('Finished pagination, generating CSV');
    profiles.forEach(profile => {
      const title = profile.querySelector('.org-people-profile-card__profile-title').innerText;
      const subtitle = profile.querySelector('.artdeco-entity-lockup__subtitle .lt-line-clamp').innerText;
      people.push([generateEmail(title, EMAIL_FORMAT), subtitle]);
    });
    
    // Combine all profiles into one CSV file
    let csvContent = people.map(e => e.join(";")).join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'emails.csv';
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } else {
    console.log('Loading more people: ' + profiles.length + '/' + pplTotal);
    if (!getPeopleRunningLock) {
      if (moreBtn) {
        moreBtn.click();
      }
    }
  }
  getPeopleRunningLock = 0;
}

let moreBtn = document.querySelector('.scaffold-finite-scroll__load-button');
const callback = (mutationList, observer) => { 
  moreBtn = document.querySelector('.scaffold-finite-scroll__load-button'); 
  if(moreBtn) { 
    moreBtn.click(); 
  } else { 
    getPeople(); 
  }
};

const peopleCardContainer = document.querySelector('.org-people-profile-card').parentElement.parentElement.parentElement;
const obs = new MutationObserver(callback);
obs.observe(peopleCardContainer, { attributes: true, childList: true, subtree: true });

// Initially run getPeople to ensure we handle the case where there is no more button
getPeople();
