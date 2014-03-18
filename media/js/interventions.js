var total_budget = 1000;

var budget_used = 0;

var update_budget_progress_bar = function() {
    var percent_used = budget_used / total_budget * 100;
    var percent_remaining = 100 - percent_used;
    var bar = $('#budget-progress-bar .progress-bar');
    bar.attr('aria-valuenow', percent_remaining);
    bar.attr('style', 'width: ' + Math.floor(percent_remaining) + "%");
    var label = $('#budget-progress-bar .sr');
    label.text("$" + (total_budget - budget_used));
};

var over_budget = function(amount) {
    $("#run-sim-button").attr('disabled','disabled');
    $("#overbudget-amount").text(amount);
    $("#overbudget").show();
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
    apply_modifiers();
    update_budget_progress_bar();
    if (budget_used > total_budget) {
        over_budget(budget_used - total_budget);
    } else {
        $("#run-sim-button").removeAttr('disabled');
        $("#overbudget").hide();
    }
};

var current_values = {};

var reset_parameters = function() {
    for (var k in defaults) {
        if (defaults.hasOwnProperty(k)) {
            $("#" + k).val(defaults[k]);
            current_values[k] = defaults[k];
        }
    }
};

var apply_modifiers = function() {
    // set everything to a known state
    reset_parameters();
    // then go through each control that is set and adjust accordingly
    var controls = $(".intervention-control");
    for (var i=0; i < controls.length; i++) {
        if (controls[i].value != "") {
            var m = modifiers[controls[i].id][controls[i].value];
            for (var j=0; j < m.length; j++) {
                var param_name = m[j].param;
                var adjustment = m[j].adjustment;
                var p = $("#" + param_name);
                var new_value = current_values[param_name] + adjustment;
                current_values[param_name] = new_value;
                p.val(new_value);
            }
        }
    }
};

$(".intervention-control").change(calculate_budget);
$("#reset-all-button").click(function () {
    reset_parameters();
    $("#intervention-form").trigger('reset');
});
