window.onload = function () {
    if(typeof app !== 'undefined') { 
        if(typeof app == 'function') { 
            let main_grid = app();
            main_grid.setAttribute("class", "uk-padding-small uk-padding-remove-vertical uk-child-width-1-2@s uk-child-width-1-3@m uk-child-width-1-6@l uk-child-width-1-6@xl uk-grid-small");
            main_grid.setAttribute("uk-grid", "");
            document.getElementById('main_contents').insertAdjacentElement("beforeend", main_grid);

            if(typeof page_title !== 'undefined') {
                let title_component = document.createElement("div"), title_header = document.createElement("h2"), el;
                title_component.classList.add("uk-padding-small", "uk-padding-remove-vertical");
                title_header.classList.add("uk-heading-bullet");
                title_header.innerText = page_title;
                title_component.appendChild(title_header);
                el = document.getElementById("main_contents");
                el.insertBefore(title_component, el.firstChild);
            }
        }
    } 
};
