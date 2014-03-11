var total_budget = 1000;

var budget_used = 0;

var update_budget_progress_bar = function() {
    var percent_used = budget_used / total_budget * 100;
    var percent_remaining = 100 - percent_used;
    var bar = $('#budget-progress-bar .progress-bar');
    bar.attr('aria-valuenow', percent_remaining);
    bar.attr('style', 'width: ' + Math.floor(percent_remaining) + "%");
    var label = $('#budget-progress-bar .sr');
    label.text("You have $" + (total_budget - budget_used) + ".00!");
};

var costs = {
    'increase-physical-activity': {
        'high': 300, 'medium': 200, 'low': 100
    },
    'ensure-screening': {
        'high': 300, 'medium': 200, 'low': 100
    },
    'active-living-at-work': {
        'high': 300, 'medium': 200, 'low': 100
    },
    'social-influence': {
        'high': 300, 'medium': 200, 'low': 100
    },
    'physical-environment': {
        'high': 300, 'medium': 200, 'low': 100
    }
};

var calculate_budget = function() {
    budget_used = 0;
    var controls = $(".intervention-control");
    for (var i=0; i < controls.length; i++) {
        if (controls[i].value != "") {
            var cost = costs[controls[i].id][controls[i].value];
            budget_used += cost;
        }
    }

    update_budget_progress_bar();
};

$(".intervention-control").change(calculate_budget);
