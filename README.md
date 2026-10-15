# Canteenio local demo

The public page and `/canteen`, `/ngo`, `/admin` workspaces are a fictional, session-local demonstration. Admin actions are open, not access-protected, and not saved to Supabase. Do not enter personal information. No Supabase queries are performed; no login, real account administration, permissions, external messaging, pickup booking, food-safety certification, or live occupancy is implemented. Changes may reset when a browser session ends or reloads and are not synchronized between independent users.

## Shared demo records

CanteenState owns food operations, requests, NGO approvals, student aggregates, breaks, notifications, fictional account labels and targeted announcements. Approval determines golden badges, request eligibility and the approved partner list. Revoked organizations cannot create or progress pickup requests; existing reservations remain until explicitly cancelled/rejected, retaining an auditable local request history.

FY initially totals 1,000 and SY 800 across the seven branches CS/CSE, ECS, IT, Mechanical, AI&DS, AI&ML and Civil. TY/BE initially use zero as an explicit unknown assumption. Each branch/year has one aggregate and a corresponding break. Percentages are validated whole values 0–100. Campus attendance, canteen visitors and meal demand are sequential rounded estimates, not observed attendance or recorded sales. Enrollment edits change totals; schedule and canteen attendance edits never change enrolled counts. Inactive schedules are omitted from active slot summaries, not from aggregate enrollment. Slot summaries group identical start times; they are not a complete overlapping-window occupancy model.

Food balance is prepared = sold + simulated collected + remaining. Listed surplus is part of remaining, and active requests reserve listed portions. Admin oversight edits the same operations and uses the same request transition guards. No financial analytics or unsupported environmental impact estimates are inferred.

Targeted announcements include year, branches, break time, manually assumed crowd and optional illustrative queue note. They appear in canteen Break planning and Notifications in the same session only, without external delivery.

The assistant is rule-based and refreshes operation/organization snapshots from central state on each question. Popularity uses recorded sold portions; remaining uses prepared minus sold minus collected. There is only an illustrative sample day, so tomorrow's preparation cannot be reliably predicted. The request did not supply the literal six prompt strings; six suggestions covering availability, popular dish, tomorrow preparation, remaining, student estimates and fictional NGO verification are provided rather than claiming an exact match to an unavailable list.

## Validation

Run the unittest suite in `tests/` for quantity balance, request transitions, enrollment distribution, atomic validation, schedule synchronization, local announcement editing and honest assistant answers. These are code-level demo checks, not live integration or production security tests.
