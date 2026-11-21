# GAM7 API coverage, deprecation and currency report

Generated 11-21-2026 by api_coverage_report.py (see script for method).

## 1. Coverage of the APIs GAM already uses

`strict` = calls the static scan could tie to this API with certainty. `loose` = also matched by name only (variable passed through a helper).

| API | version | Google methods | called (strict) | called (strict+loose) |
|---|---|---|---|---|
| accesscontextmanager | v1 | 42 | 0 | 7 |
| admin | datatransfer_v1 | 5 | 4 | 4 |
| admin | directory_v1 | 128 | 92 | 99 |
| admin | reports_v1 | 6 | 3 | 3 |
| alertcenter | v1beta1 | 11 | 8 | 8 |
| analyticsadmin | v1beta | 55 | 4 | 4 |
| calendar-json | v3 | 38 | 7 | 19 |
| chat | v1 | 56 | 26 | 33 |
| chromemanagement | v1 | 71 | 21 | 26 |
| chromepolicy | v1 | 14 | 6 | 6 |
| classroom | v1 | 105 | 28 | 35 |
| cloudchannel | v1 | 65 | 5 | 6 |
| cloudidentity | v1 | 70 | 38 | 51 |
| cloudidentity | v1beta1 | 71 | 2 | 18 |
| cloudresourcemanager | v1 | 38 | 0 | 8 |
| cloudresourcemanager | v3 | 92 | 3 | 11 |
| docs | v1 | 3 | 2 | 2 |
| drive | v2 | 75 | 1 | 24 |
| drive | v3 | 64 | 17 | 29 |
| driveactivity | v2 | 1 | 1 | 1 |
| drivelabels | v2 | 26 | 0 | 9 |
| forms | v1 | 10 | 4 | 4 |
| gmail | v1 | 79 | 38 | 43 |
| groupsmigration | v1 | 1 | 1 | 1 |
| groupssettings | v1 | 3 | 2 | 3 |
| iam | v1 | 137 | 9 | 19 |
| iamcredentials | v1 | 7 | 1 | 1 |
| keep | v1 | 7 | 4 | 6 |
| licensing | v1 | 7 | 3 | 6 |
| meet | v2 | 24 | 8 | 13 |
| mybusinessaccountmanagement | v1 | 16 | 1 | 1 |
| oauth2 | v2 | 3 | 1 | 1 |
| orgpolicy | v2 | 26 | 0 | 0 |
| people | v1 | 24 | 16 | 16 |
| pubsub | v1 | 46 | 7 | 7 |
| reseller | v1 | 17 | 13 | 13 |
| searchconsole | v1 | 11 | 1 | 1 |
| servicemanagement | v1 | 22 | 0 | 1 |
| serviceusage | v1 | 10 | 2 | 3 |
| sheets | v4 | 17 | 3 | 7 |
| siteVerification | v1 | 7 | 3 | 3 |
| storage | v1 | 86 | 3 | 4 |
| tagmanager | v2 | 106 | 0 | 1 |
| tasks | v1 | 14 | 4 | 12 |
| vault | v1 | 33 | 23 | 23 |
| versionhistory | v1 | 4 | 4 | 4 |
| youtube | v3 | 83 | 1 | 2 |

## 2. Methods GAM calls that Google marks deprecated

None found (checked the `deprecated` flag and descriptions that start with the word Deprecated).

## 3. API version currency

| GAM name | GAM version | Google's preferred version | all versions Google lists | note |
|---|---|---|---|---|
| alertcenter | v1beta1 | v1beta1 | v1beta1 | GAM uses a pre-release version |
| analyticsadmin | v1beta | v1beta | v1beta, v1alpha | GAM uses a pre-release version |
| cloudidentitygroupsbeta | v1beta1 | v1 | v1beta1, v1 | newer preferred version exists |
| cloudidentityorgunitsbeta | v1beta1 | v1 | v1beta1, v1 | newer preferred version exists |
| cloudresourcemanagerv1 | v1 | v3 | v1beta1, v1, v2beta1, v2, v3 | newer preferred version exists |
| drive2 | v2 | v3 | v2, v3 | newer preferred version exists |
| iam | v1 | v2 | v1, v2beta, v2 | newer preferred version exists |

## 4. Workspace-relevant Google APIs GAM does not use at all

| API | latest version | why an administrator might care |
|---|---|---|
| androiddeviceprovisioning | v1 | Android Device Provisioning: zero-touch enrollment |
| androidmanagement | v1 | Android Management API: Android Enterprise devices and policies |
| appsmarket | v2 | Workspace Marketplace API: inspect Marketplace apps / licenses installed in the domain |
| chromewebstore | v2 | Chrome Web Store API: inspect/publish extension items |
| cloudasset | v1 | Cloud Asset Inventory: IAM/policy search across the organization |
| cloudsearch | v1 | Cloud Search API: enterprise search data sources, identity sources, indexing |
| dataportability | v1 | Data Portability API: export a user's Google data (offboarding / legal requests) |
| gmailpostmastertools | v2 | Gmail Postmaster Tools: domain reputation, spam rate, SPF/DKIM/DMARC delivery stats |
| logging | v2 | Cloud Logging: query audit logs exported to Cloud Logging |
| marketingplatformadmin | v1alpha | Google Marketing Platform admin: org/account links |
| mybusinessbusinessinformation | v1 | Business Profile information (GAM only uses account management) |
| script | v1 | Apps Script API: manage/deploy script projects, view execution metrics |
| securitycenter | v1 | Security Command Center: findings and posture |
| slides | v1 | Slides API: read/create/update presentations (GAM has Docs, Sheets and Forms but not Slides) |
| verifiedaccess | v2 | Chrome Verified Access API: device attestation for Zero Trust |
| workspaceevents | v1 | Workspace Events API: subscriptions to Drive/Chat/Meet events (push notifications) |

## 5. Methods Google offers that GAM never calls (per API)

### accesscontextmanager v1 (35 not called)

`accessPolicies.create`, `accessPolicies.delete`, `accessPolicies.get`, `accessPolicies.getIamPolicy`, `accessPolicies.patch`, `accessPolicies.setIamPolicy`, `accessPolicies.testIamPermissions`, `accessPolicies/accessLevels.get`, `accessPolicies/accessLevels.replaceAll`, `accessPolicies/accessLevels.testIamPermissions`, `accessPolicies/authorizedOrgsDescs.create`, `accessPolicies/authorizedOrgsDescs.delete`, `accessPolicies/authorizedOrgsDescs.get`, `accessPolicies/authorizedOrgsDescs.list`, `accessPolicies/authorizedOrgsDescs.patch`, `accessPolicies/servicePerimeters.commit`, `accessPolicies/servicePerimeters.create`, `accessPolicies/servicePerimeters.delete`, `accessPolicies/servicePerimeters.get`, `accessPolicies/servicePerimeters.list`, `accessPolicies/servicePerimeters.patch`, `accessPolicies/servicePerimeters.replaceAll`, `accessPolicies/servicePerimeters.testIamPermissions`, `folders.lookupConfiguredServicePerimeter`, `operations.cancel`, `operations.delete`, `operations.list`, `organizations/gcpUserAccessBindings.create`, `organizations/gcpUserAccessBindings.delete`, `organizations/gcpUserAccessBindings.get`, `organizations/gcpUserAccessBindings.list`, `organizations/gcpUserAccessBindings.patch`, `projects.lookupConfiguredServicePerimeter`, `services.get`, `services.list`

### admin datatransfer_v1 (1 not called)

`applications.get`

### admin directory_v1 (29 not called)

`asps.get`, `channels.stop`, `chromeosdevices.action`, `customer/devices/chromeos.countChromeOsDevices`, `customers/chrome/printServers.batchCreatePrintServers`, `customers/chrome/printServers.batchDeletePrintServers`, `customers/chrome/printServers.create`, `customers/chrome/printServers.delete`, `customers/chrome/printServers.get`, `customers/chrome/printServers.list`, `customers/chrome/printServers.patch`, `customers/chrome/printers.batchCreatePrinters`, `customers/chrome/printers.delete`, `members.hasMember`, `members.update`, `orgunits.patch`, `resources/buildings.update`, `resources/calendars.update`, `resources/features.get`, `resources/features.patch`, `resources/features.update`, `roleAssignments.get`, `roles.update`, `schemas.patch`, `users.makeAdmin`, `users.patch`, `users.watch`, `users/aliases.watch`, `users/photos.patch`

### admin reports_v1 (3 not called)

`activities.watch`, `channels.stop`, `entityUsageReports.get`

### alertcenter v1beta1 (3 not called)

`alerts.batchDelete`, `alerts.batchUndelete`, `alerts.getMetadata`

### analyticsadmin v1beta (51 not called)

`accounts.delete`, `accounts.get`, `accounts.getDataSharingSettings`, `accounts.patch`, `accounts.provisionAccountTicket`, `accounts.runAccessReport`, `accounts.searchChangeHistoryEvents`, `properties.acknowledgeUserDataCollection`, `properties.create`, `properties.delete`, `properties.get`, `properties.getDataRetentionSettings`, `properties.patch`, `properties.runAccessReport`, `properties.updateDataRetentionSettings`, `properties/conversionEvents.create`, `properties/conversionEvents.delete`, `properties/conversionEvents.get`, `properties/conversionEvents.list`, `properties/conversionEvents.patch`, `properties/customDimensions.archive`, `properties/customDimensions.create`, `properties/customDimensions.get`, `properties/customDimensions.list`, `properties/customDimensions.patch`, `properties/customMetrics.archive`, `properties/customMetrics.create`, `properties/customMetrics.get`, `properties/customMetrics.list`, `properties/customMetrics.patch`, `properties/dataStreams.create`, `properties/dataStreams.delete`, `properties/dataStreams.get`, `properties/dataStreams.patch`, `properties/dataStreams/measurementProtocolSecrets.create`, `properties/dataStreams/measurementProtocolSecrets.delete`, `properties/dataStreams/measurementProtocolSecrets.get`, `properties/dataStreams/measurementProtocolSecrets.list`, `properties/dataStreams/measurementProtocolSecrets.patch`, `properties/firebaseLinks.create`, `properties/firebaseLinks.delete`, `properties/firebaseLinks.list`, `properties/googleAdsLinks.create`, `properties/googleAdsLinks.delete`, `properties/googleAdsLinks.list`, `properties/googleAdsLinks.patch`, `properties/keyEvents.create`, `properties/keyEvents.delete`, `properties/keyEvents.get`, `properties/keyEvents.list`, `properties/keyEvents.patch`

### calendar-json v3 (19 not called)

`acl.delete`, `acl.insert`, `acl.patch`, `acl.update`, `acl.watch`, `calendarList.delete`, `calendarList.insert`, `calendarList.patch`, `calendarList.update`, `calendarList.watch`, `calendars.update`, `channels.stop`, `colors.get`, `events.quickAdd`, `events.update`, `events.watch`, `freebusy.query`, `settings.get`, `settings.watch`

### chat v1 (23 not called)

`media.download`, `media.upload`, `spaces.completeImport`, `spaces.create`, `spaces.findGroupChats`, `spaces/messagePins.create`, `spaces/messagePins.delete`, `spaces/messagePins.list`, `spaces/messages.replaceCards`, `spaces/messages.update`, `spaces/messages/attachments.get`, `spaces/messages/reactions.create`, `spaces/messages/reactions.delete`, `spaces/messages/reactions.list`, `users/availability.markAsActive`, `users/availability.markAsAway`, `users/availability.markAsDoNotDisturb`, `users/spaces.getSpaceReadState`, `users/spaces.updateSpaceReadState`, `users/spaces/spaceNotificationSetting.get`, `users/spaces/spaceNotificationSetting.patch`, `users/spaces/threads.getThreadReadState`, `users/spaces/threads.updateThreadReadState`

### chromemanagement v1 (45 not called)

`customers.getSubscriptionInfo`, `customers/apps.countChromeAppRequests`, `customers/apps.fetchDevicesRequestingExtension`, `customers/apps.fetchUsersRequestingExtension`, `customers/certificateProvisioningProcesses.claim`, `customers/certificateProvisioningProcesses.get`, `customers/certificateProvisioningProcesses.setFailure`, `customers/certificateProvisioningProcesses.signData`, `customers/certificateProvisioningProcesses.uploadCertificate`, `customers/connectorConfigs.create`, `customers/connectorConfigs.delete`, `customers/connectorConfigs.get`, `customers/connectorConfigs.list`, `customers/connectorConfigs.patch`, `customers/enterprise/securityInsights.checkEnablementStatus`, `customers/enterprise/securityInsights.disable`, `customers/enterprise/securityInsights.enable`, `customers/enterprise/securityInsights.queryContentTransfers`, `customers/enterprise/securityInsights.queryContentTransfersBreakdowns`, `customers/enterprise/securityInsights.queryUrlVisits`, `customers/enterprise/securityInsights.queryUrlVisitsBreakdowns`, `customers/reports.countActiveDevices`, `customers/reports.countChromeBrowsersNeedingAttention`, `customers/reports.countChromeCrashEvents`, `customers/reports.countChromeDevicesReachingAutoExpirationDate`, `customers/reports.countChromeHardwareFleetDevices`, `customers/reports.countChromeProfileVersions`, `customers/reports.countDevicesPerBootType`, `customers/reports.countDevicesPerReleaseChannel`, `customers/reports.countPrintJobsByPrinter`, `customers/reports.countPrintJobsByUser`, `customers/reports.enumeratePrintJobs`, `customers/reports.findInstalledAppProfiles`, `customers/reports.findSaasUsage`, `customers/reports.findSaasUsageBrowsers`, `customers/reports.findSaasUsageProfiles`, `customers/telemetry/notificationConfigs.create`, `customers/telemetry/notificationConfigs.delete`, `customers/telemetry/notificationConfigs.list`, `customers/telemetry/users.get`, `customers/telemetry/users.list`, `customers/thirdPartyProfileUsers.move`, `operations.cancel`, `operations.delete`, `operations.list`

### chromepolicy v1 (8 not called)

`customers/policies/groups.batchDelete`, `customers/policies/groups.batchModify`, `customers/policies/groups.listGroupPriorityOrdering`, `customers/policies/groups.updateGroupPriorityOrdering`, `customers/policies/networks.defineCertificate`, `customers/policies/networks.removeCertificate`, `customers/policies/orgunits.batchInherit`, `customers/policies/orgunits.batchModify`

### classroom v1 (70 not called)

`courses.getGradingPeriodSettings`, `courses.update`, `courses.updateGradingPeriodSettings`, `courses/aliases.delete`, `courses/announcements.delete`, `courses/announcements.getAddOnContext`, `courses/announcements.modifyAssignees`, `courses/announcements.patch`, `courses/announcements/addOnAttachments.create`, `courses/announcements/addOnAttachments.delete`, `courses/announcements/addOnAttachments.get`, `courses/announcements/addOnAttachments.list`, `courses/announcements/addOnAttachments.patch`, `courses/courseWork.create`, `courses/courseWork.delete`, `courses/courseWork.getAddOnContext`, `courses/courseWork.modifyAssignees`, `courses/courseWork.patch`, `courses/courseWork.updateRubric`, `courses/courseWork/addOnAttachments.create`, `courses/courseWork/addOnAttachments.delete`, `courses/courseWork/addOnAttachments.get`, `courses/courseWork/addOnAttachments.list`, `courses/courseWork/addOnAttachments.patch`, `courses/courseWork/addOnAttachments/studentSubmissions.get`, `courses/courseWork/addOnAttachments/studentSubmissions.list`, `courses/courseWork/addOnAttachments/studentSubmissions.patch`, `courses/courseWork/rubrics.create`, `courses/courseWork/rubrics.delete`, `courses/courseWork/rubrics.get`, `courses/courseWork/rubrics.list`, `courses/courseWork/rubrics.patch`, `courses/courseWork/studentSubmissions.modifyAttachments`, `courses/courseWork/studentSubmissions.patch`, `courses/courseWork/studentSubmissions.reclaim`, `courses/courseWork/studentSubmissions.return`, `courses/courseWork/studentSubmissions.turnIn`, `courses/courseWorkMaterials.create`, `courses/courseWorkMaterials.delete`, `courses/courseWorkMaterials.getAddOnContext`, `courses/courseWorkMaterials.patch`, `courses/courseWorkMaterials/addOnAttachments.create`, `courses/courseWorkMaterials/addOnAttachments.delete`, `courses/courseWorkMaterials/addOnAttachments.get`, `courses/courseWorkMaterials/addOnAttachments.list`, `courses/courseWorkMaterials/addOnAttachments.patch`, `courses/posts.getAddOnContext`, `courses/posts/addOnAttachments.create`, `courses/posts/addOnAttachments.delete`, `courses/posts/addOnAttachments.get`, `courses/posts/addOnAttachments.list`, `courses/posts/addOnAttachments.patch`, `courses/posts/addOnAttachments/studentSubmissions.get`, `courses/posts/addOnAttachments/studentSubmissions.patch`, `courses/studentGroups/studentGroupMembers.create`, `courses/studentGroups/studentGroupMembers.delete`, `courses/students.delete`, `courses/students.get`, `courses/teachers.delete`, `courses/teachers.get`, `courses/topics.delete`, `courses/topics.patch`, `invitations.accept`, `invitations.create`, `invitations.delete`, `invitations.get`, `registrations.create`, `registrations.delete`, `userProfiles/guardianInvitations.get`, `userProfiles/guardians.get`

### cloudchannel v1 (59 not called)

`accounts.checkCloudIdentityAccountsExist`, `accounts.listSubscribers`, `accounts.listTransferableOffers`, `accounts.listTransferableSkus`, `accounts.register`, `accounts.unregister`, `accounts/channelPartnerLinks.create`, `accounts/channelPartnerLinks.get`, `accounts/channelPartnerLinks.list`, `accounts/channelPartnerLinks.patch`, `accounts/channelPartnerLinks/channelPartnerRepricingConfigs.create`, `accounts/channelPartnerLinks/channelPartnerRepricingConfigs.delete`, `accounts/channelPartnerLinks/channelPartnerRepricingConfigs.get`, `accounts/channelPartnerLinks/channelPartnerRepricingConfigs.list`, `accounts/channelPartnerLinks/channelPartnerRepricingConfigs.patch`, `accounts/channelPartnerLinks/customers.create`, `accounts/channelPartnerLinks/customers.delete`, `accounts/channelPartnerLinks/customers.get`, `accounts/channelPartnerLinks/customers.import`, `accounts/channelPartnerLinks/customers.list`, `accounts/channelPartnerLinks/customers.patch`, `accounts/customers.create`, `accounts/customers.delete`, `accounts/customers.get`, `accounts/customers.import`, `accounts/customers.listPurchasableOffers`, `accounts/customers.listPurchasableSkus`, `accounts/customers.patch`, `accounts/customers.provisionCloudIdentity`, `accounts/customers.queryEligibleBillingAccounts`, `accounts/customers.transferEntitlements`, `accounts/customers.transferEntitlementsToGoogle`, `accounts/customers/customerRepricingConfigs.create`, `accounts/customers/customerRepricingConfigs.delete`, `accounts/customers/customerRepricingConfigs.get`, `accounts/customers/customerRepricingConfigs.list`, `accounts/customers/customerRepricingConfigs.patch`, `accounts/customers/entitlements.activate`, `accounts/customers/entitlements.cancel`, `accounts/customers/entitlements.changeOffer`, `accounts/customers/entitlements.changeParameters`, `accounts/customers/entitlements.changeRenewalSettings`, `accounts/customers/entitlements.create`, `accounts/customers/entitlements.get`, `accounts/customers/entitlements.listEntitlementChanges`, `accounts/customers/entitlements.lookupOffer`, `accounts/customers/entitlements.startPaidService`, `accounts/customers/entitlements.suspend`, `accounts/reportJobs.fetchReportResults`, `accounts/reports.list`, `accounts/reports.run`, `accounts/skuGroups.list`, `accounts/skuGroups/billableSkus.list`, `integrators.listSubscribers`, `integrators.registerSubscriber`, `integrators.unregisterSubscriber`, `operations.cancel`, `operations.delete`, `operations.list`

### cloudidentity v1 (19 not called)

`devices.cancelWipe`, `devices.delete`, `devices.wipe`, `devices/deviceUsers.approve`, `devices/deviceUsers.block`, `devices/deviceUsers.cancelWipe`, `devices/deviceUsers.delete`, `devices/deviceUsers.lookup`, `devices/deviceUsers.wipe`, `groups/memberships.checkTransitiveMembership`, `groups/memberships.lookup`, `groups/memberships.searchDirectGroups`, `inboundOidcSsoProfiles.create`, `inboundOidcSsoProfiles.delete`, `inboundOidcSsoProfiles.patch`, `inboundSamlSsoProfiles.create`, `inboundSamlSsoProfiles.delete`, `inboundSamlSsoProfiles.patch`, `inboundSamlSsoProfiles/idpCredentials.add`

### cloudidentity v1beta1 (53 not called)

`allowlistedDomains.create`, `allowlistedDomains.delete`, `allowlistedDomains.get`, `allowlistedDomains.list`, `customers/userinvitations.list`, `devices.cancelWipe`, `devices.delete`, `devices.wipe`, `devices/deviceUsers.approve`, `devices/deviceUsers.block`, `devices/deviceUsers.cancelWipe`, `devices/deviceUsers.delete`, `devices/deviceUsers.lookup`, `devices/deviceUsers.wipe`, `groups.delete`, `groups.getSecuritySettings`, `groups.lookup`, `groups.updateSecuritySettings`, `groups/memberships.checkTransitiveMembership`, `groups/memberships.create`, `groups/memberships.delete`, `groups/memberships.get`, `groups/memberships.getMembershipGraph`, `groups/memberships.list`, `groups/memberships.lookup`, `groups/memberships.modifyMembershipRoles`, `groups/memberships.searchDirectGroups`, `groups/memberships.searchTransitiveGroups`, `groups/memberships.searchTransitiveMemberships`, `inboundOidcSsoProfiles.create`, `inboundOidcSsoProfiles.delete`, `inboundOidcSsoProfiles.get`, `inboundOidcSsoProfiles.list`, `inboundOidcSsoProfiles.patch`, `inboundSamlSsoProfiles.create`, `inboundSamlSsoProfiles.delete`, `inboundSamlSsoProfiles.get`, `inboundSamlSsoProfiles.list`, `inboundSamlSsoProfiles.patch`, `inboundSamlSsoProfiles/idpCredentials.add`, `inboundSamlSsoProfiles/idpCredentials.delete`, `inboundSamlSsoProfiles/idpCredentials.get`, `inboundSamlSsoProfiles/idpCredentials.list`, `inboundSsoAssignments.create`, `inboundSsoAssignments.delete`, `inboundSsoAssignments.get`, `inboundSsoAssignments.list`, `inboundSsoAssignments.patch`, `policies.create`, `policies.delete`, `policies.get`, `policies.list`, `policies.patch`

### cloudresourcemanager v1 (30 not called)

`folders.clearOrgPolicy`, `folders.getEffectiveOrgPolicy`, `folders.getOrgPolicy`, `folders.listAvailableOrgPolicyConstraints`, `folders.listOrgPolicies`, `folders.setOrgPolicy`, `liens.create`, `liens.delete`, `liens.get`, `liens.list`, `organizations.clearOrgPolicy`, `organizations.get`, `organizations.getEffectiveOrgPolicy`, `organizations.getOrgPolicy`, `organizations.listAvailableOrgPolicyConstraints`, `organizations.listOrgPolicies`, `organizations.setOrgPolicy`, `organizations.testIamPermissions`, `projects.clearOrgPolicy`, `projects.get`, `projects.getEffectiveOrgPolicy`, `projects.getOrgPolicy`, `projects.list`, `projects.listAvailableOrgPolicyConstraints`, `projects.listOrgPolicies`, `projects.setIamPolicy`, `projects.setOrgPolicy`, `projects.testIamPermissions`, `projects.undelete`, `projects.update`

### cloudresourcemanager v3 (81 not called)

`effectiveTags.list`, `folders.delete`, `folders.get`, `folders.getBoundaryConfig`, `folders.getIamPolicy`, `folders.list`, `folders.move`, `folders.patch`, `folders.setIamPolicy`, `folders.testIamPermissions`, `folders.undelete`, `folders.updateBoundaryConfig`, `folders/boundaries.create`, `folders/boundaries.delete`, `folders/boundaries.get`, `folders/boundaries.list`, `folders/boundaries.patch`, `folders/capabilities.get`, `folders/capabilities.patch`, `folders/capabilityConfigs.create`, `folders/capabilityConfigs.delete`, `folders/capabilityConfigs.get`, `folders/capabilityConfigs.list`, `folders/capabilityConfigs.patch`, `liens.create`, `liens.delete`, `liens.get`, `liens.list`, `locations/effectiveTagBindingCollections.get`, `locations/tagBindingCollections.get`, `locations/tagBindingCollections.patch`, `organizations.get`, `organizations.getBoundaryConfig`, `organizations.testIamPermissions`, `organizations.updateBoundaryConfig`, `organizations/boundaries.create`, `organizations/boundaries.delete`, `organizations/boundaries.get`, `organizations/boundaries.list`, `organizations/boundaries.patch`, `organizations/capabilityConfigs.create`, `organizations/capabilityConfigs.delete`, `organizations/capabilityConfigs.get`, `organizations/capabilityConfigs.list`, `organizations/capabilityConfigs.patch`, `projects.list`, `projects.move`, `projects.patch`, `projects.setIamPolicy`, `projects.testIamPermissions`, `projects.undelete`, `projects/capabilityConfigs.create`, `projects/capabilityConfigs.delete`, `projects/capabilityConfigs.get`, `projects/capabilityConfigs.list`, `projects/capabilityConfigs.patch`, `tagBindings.create`, `tagBindings.delete`, `tagBindings.list`, `tagKeys.create`, `tagKeys.delete`, `tagKeys.get`, `tagKeys.getIamPolicy`, `tagKeys.getNamespaced`, `tagKeys.list`, `tagKeys.patch`, `tagKeys.setIamPolicy`, `tagKeys.testIamPermissions`, `tagValues.create`, `tagValues.delete`, `tagValues.get`, `tagValues.getIamPolicy`, `tagValues.getNamespaced`, `tagValues.list`, `tagValues.patch`, `tagValues.setIamPolicy`, `tagValues.testIamPermissions`, `tagValues/tagHolds.create`, `tagValues/tagHolds.delete`, `tagValues/tagHolds.list`, `v3.fetchResourceSemantics`

### docs v1 (1 not called)

`documents.create`

### drive v2 (51 not called)

`apps.get`, `apps.list`, `changes.get`, `changes.getStartPageToken`, `changes.list`, `changes.watch`, `channels.stop`, `children.delete`, `children.get`, `children.insert`, `children.list`, `comments.delete`, `comments.get`, `comments.insert`, `comments.patch`, `comments.update`, `drives.insert`, `files.emptyTrash`, `files.export`, `files.generateCseToken`, `files.generateIds`, `files.insert`, `files.patch`, `files.touch`, `files.trash`, `files.untrash`, `files.watch`, `parents.delete`, `parents.get`, `parents.insert`, `parents.list`, `permissions.insert`, `permissions.patch`, `properties.delete`, `properties.get`, `properties.insert`, `properties.list`, `properties.patch`, `properties.update`, `replies.delete`, `replies.get`, `replies.insert`, `replies.list`, `replies.patch`, `replies.update`, `revisions.patch`, `teamdrives.delete`, `teamdrives.get`, `teamdrives.insert`, `teamdrives.list`, `teamdrives.update`

### drive v3 (35 not called)

`accessproposals.get`, `accessproposals.list`, `accessproposals.resolve`, `approvals.approve`, `approvals.cancel`, `approvals.comment`, `approvals.decline`, `approvals.get`, `approvals.list`, `approvals.reassign`, `approvals.start`, `apps.get`, `apps.list`, `changes.list`, `changes.watch`, `channels.stop`, `comments.create`, `comments.delete`, `comments.get`, `comments.update`, `files.download`, `files.export`, `files.generateCseToken`, `files.generateIds`, `files.watch`, `replies.create`, `replies.delete`, `replies.get`, `replies.list`, `replies.update`, `teamdrives.create`, `teamdrives.delete`, `teamdrives.get`, `teamdrives.list`, `teamdrives.update`

### drivelabels v2 (17 not called)

`labels.create`, `labels.delete`, `labels.delta`, `labels.disable`, `labels.enable`, `labels.publish`, `labels.updateLabelCopyMode`, `labels.updateLabelEnabledAppSettings`, `labels.updatePermissions`, `labels/locks.list`, `labels/permissions.batchUpdate`, `labels/revisions.updatePermissions`, `labels/revisions/locks.list`, `labels/revisions/permissions.batchDelete`, `labels/revisions/permissions.batchUpdate`, `limits.getLabel`, `users.getCapabilities`

### forms v1 (6 not called)

`forms.create`, `forms/responses.get`, `forms/watches.create`, `forms/watches.delete`, `forms/watches.list`, `forms/watches.renew`

### gmail v1 (36 not called)

`users.stop`, `users.watch`, `users/drafts.delete`, `users/drafts.get`, `users/drafts.list`, `users/drafts.send`, `users/drafts.update`, `users/history.list`, `users/labels.update`, `users/messages.batchDelete`, `users/messages.batchModify`, `users/messages.delete`, `users/messages.trash`, `users/messages.untrash`, `users/settings/cse/identities.delete`, `users/settings/cse/identities.get`, `users/settings/cse/identities.patch`, `users/settings/cse/keypairs.disable`, `users/settings/cse/keypairs.enable`, `users/settings/cse/keypairs.get`, `users/settings/cse/keypairs.obliterate`, `users/settings/delegates.get`, `users/settings/forwardingAddresses.create`, `users/settings/forwardingAddresses.delete`, `users/settings/forwardingAddresses.get`, `users/settings/sendAs.create`, `users/settings/sendAs.delete`, `users/settings/sendAs.patch`, `users/settings/sendAs.update`, `users/settings/sendAs.verify`, `users/settings/sendAs/smimeInfo.get`, `users/threads.delete`, `users/threads.list`, `users/threads.modify`, `users/threads.trash`, `users/threads.untrash`

### iam v1 (118 not called)

`iamPolicies.lintPolicy`, `iamPolicies.queryAuditableServices`, `locations/workforcePools.create`, `locations/workforcePools.delete`, `locations/workforcePools.get`, `locations/workforcePools.getIamPolicy`, `locations/workforcePools.list`, `locations/workforcePools.patch`, `locations/workforcePools.setIamPolicy`, `locations/workforcePools.testIamPermissions`, `locations/workforcePools.undelete`, `locations/workforcePools/providers.create`, `locations/workforcePools/providers.delete`, `locations/workforcePools/providers.get`, `locations/workforcePools/providers.list`, `locations/workforcePools/providers.patch`, `locations/workforcePools/providers.undelete`, `locations/workforcePools/providers/keys.create`, `locations/workforcePools/providers/keys.delete`, `locations/workforcePools/providers/keys.get`, `locations/workforcePools/providers/keys.list`, `locations/workforcePools/providers/keys.undelete`, `locations/workforcePools/providers/scimTenants.create`, `locations/workforcePools/providers/scimTenants.delete`, `locations/workforcePools/providers/scimTenants.get`, `locations/workforcePools/providers/scimTenants.getIamPolicy`, `locations/workforcePools/providers/scimTenants.list`, `locations/workforcePools/providers/scimTenants.patch`, `locations/workforcePools/providers/scimTenants.setIamPolicy`, `locations/workforcePools/providers/scimTenants.testIamPermissions`, `locations/workforcePools/providers/scimTenants.undelete`, `locations/workforcePools/providers/scimTenants/tokens.create`, `locations/workforcePools/providers/scimTenants/tokens.delete`, `locations/workforcePools/providers/scimTenants/tokens.get`, `locations/workforcePools/providers/scimTenants/tokens.list`, `locations/workforcePools/providers/scimTenants/tokens.patch`, `locations/workforcePools/subjects.delete`, `locations/workforcePools/subjects.revokeSessions`, `locations/workforcePools/subjects.undelete`, `organizations/roles.create`, `organizations/roles.delete`, `organizations/roles.get`, `organizations/roles.list`, `organizations/roles.patch`, `organizations/roles.undelete`, `permissions.queryTestablePermissions`, `projects/locations/oauthClients.create`, `projects/locations/oauthClients.delete`, `projects/locations/oauthClients.get`, `projects/locations/oauthClients.list`, `projects/locations/oauthClients.patch`, `projects/locations/oauthClients.undelete`, `projects/locations/oauthClients/credentials.create`, `projects/locations/oauthClients/credentials.delete`, `projects/locations/oauthClients/credentials.get`, `projects/locations/oauthClients/credentials.list`, `projects/locations/oauthClients/credentials.patch`, `projects/locations/workloadIdentityPools.addAttestationRule`, `projects/locations/workloadIdentityPools.create`, `projects/locations/workloadIdentityPools.delete`, `projects/locations/workloadIdentityPools.get`, `projects/locations/workloadIdentityPools.getIamPolicy`, `projects/locations/workloadIdentityPools.list`, `projects/locations/workloadIdentityPools.listAttestationRules`, `projects/locations/workloadIdentityPools.patch`, `projects/locations/workloadIdentityPools.removeAttestationRule`, `projects/locations/workloadIdentityPools.setAttestationRules`, `projects/locations/workloadIdentityPools.setIamPolicy`, `projects/locations/workloadIdentityPools.testIamPermissions`, `projects/locations/workloadIdentityPools.undelete`, `projects/locations/workloadIdentityPools/namespaces.create`, `projects/locations/workloadIdentityPools/namespaces.delete`, `projects/locations/workloadIdentityPools/namespaces.get`, `projects/locations/workloadIdentityPools/namespaces.list`, `projects/locations/workloadIdentityPools/namespaces.patch`, `projects/locations/workloadIdentityPools/namespaces.undelete`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.addAttestationRule`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.create`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.delete`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.get`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.list`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.listAttestationRules`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.patch`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.removeAttestationRule`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.setAttestationRules`, `projects/locations/workloadIdentityPools/namespaces/managedIdentities.undelete`, `projects/locations/workloadIdentityPools/providers.create`, `projects/locations/workloadIdentityPools/providers.delete`, `projects/locations/workloadIdentityPools/providers.get`, `projects/locations/workloadIdentityPools/providers.list`, `projects/locations/workloadIdentityPools/providers.patch`, `projects/locations/workloadIdentityPools/providers.undelete`, `projects/locations/workloadIdentityPools/providers/keys.create`, `projects/locations/workloadIdentityPools/providers/keys.delete`, `projects/locations/workloadIdentityPools/providers/keys.get`, `projects/locations/workloadIdentityPools/providers/keys.list`, `projects/locations/workloadIdentityPools/providers/keys.undelete`, `projects/roles.create`, `projects/roles.delete`, `projects/roles.get`, `projects/roles.list`, `projects/roles.patch`, `projects/roles.undelete`, `projects/serviceAccounts.disable`, `projects/serviceAccounts.enable`, `projects/serviceAccounts.get`, `projects/serviceAccounts.getIamPolicy`, `projects/serviceAccounts.patch`, `projects/serviceAccounts.signBlob`, `projects/serviceAccounts.signJwt`, `projects/serviceAccounts.testIamPermissions`, `projects/serviceAccounts.undelete`, `projects/serviceAccounts.update`, `projects/serviceAccounts/keys.disable`, `projects/serviceAccounts/keys.enable`, `roles.get`, `roles.list`, `roles.queryGrantableRoles`

### iamcredentials v1 (6 not called)

`locations/workforcePools.getAllowedLocations`, `projects/locations/workloadIdentityPools.getAllowedLocations`, `projects/serviceAccounts.generateAccessToken`, `projects/serviceAccounts.generateIdToken`, `projects/serviceAccounts.getAllowedLocations`, `projects/serviceAccounts.signBlob`

### keep v1 (1 not called)

`media.download`

### licensing v1 (1 not called)

`licenseAssignments.update`

### meet v2 (11 not called)

`conferenceRecords.get`, `conferenceRecords/participants.get`, `conferenceRecords/participants/participantSessions.get`, `conferenceRecords/participants/participantSessions.list`, `conferenceRecords/recordings.get`, `conferenceRecords/smartNotes.get`, `conferenceRecords/smartNotes.list`, `conferenceRecords/transcripts.get`, `conferenceRecords/transcripts/entries.get`, `conferenceRecords/transcripts/entries.list`, `spaces/members.batchUpdate`

### mybusinessaccountmanagement v1 (15 not called)

`accounts.create`, `accounts.get`, `accounts.patch`, `accounts/admins.create`, `accounts/admins.delete`, `accounts/admins.list`, `accounts/admins.patch`, `accounts/invitations.accept`, `accounts/invitations.decline`, `accounts/invitations.list`, `locations.transfer`, `locations/admins.create`, `locations/admins.delete`, `locations/admins.list`, `locations/admins.patch`

### oauth2 v2 (2 not called)

`userinfo.get`, `userinfo/v2/me.get`

### orgpolicy v2 (26 not called)

`folders/constraints.list`, `folders/policies.create`, `folders/policies.delete`, `folders/policies.get`, `folders/policies.getEffectivePolicy`, `folders/policies.list`, `folders/policies.patch`, `organizations/constraints.list`, `organizations/customConstraints.create`, `organizations/customConstraints.delete`, `organizations/customConstraints.get`, `organizations/customConstraints.list`, `organizations/customConstraints.patch`, `organizations/policies.create`, `organizations/policies.delete`, `organizations/policies.get`, `organizations/policies.getEffectivePolicy`, `organizations/policies.list`, `organizations/policies.patch`, `projects/constraints.list`, `projects/policies.create`, `projects/policies.delete`, `projects/policies.get`, `projects/policies.getEffectivePolicy`, `projects/policies.list`, `projects/policies.patch`

### people v1 (8 not called)

`contactGroups.batchGet`, `contactGroups/members.modify`, `people.batchCreateContacts`, `people.batchDeleteContacts`, `people.batchUpdateContacts`, `people.deleteContactPhoto`, `people.getBatchGet`, `people.updateContactPhoto`

### pubsub v1 (39 not called)

`projects/schemas.commit`, `projects/schemas.create`, `projects/schemas.delete`, `projects/schemas.deleteRevision`, `projects/schemas.get`, `projects/schemas.getIamPolicy`, `projects/schemas.list`, `projects/schemas.listRevisions`, `projects/schemas.rollback`, `projects/schemas.setIamPolicy`, `projects/schemas.testIamPermissions`, `projects/schemas.validate`, `projects/schemas.validateMessage`, `projects/snapshots.create`, `projects/snapshots.delete`, `projects/snapshots.get`, `projects/snapshots.getIamPolicy`, `projects/snapshots.list`, `projects/snapshots.patch`, `projects/snapshots.setIamPolicy`, `projects/snapshots.testIamPermissions`, `projects/subscriptions.delete`, `projects/subscriptions.detach`, `projects/subscriptions.get`, `projects/subscriptions.getIamPolicy`, `projects/subscriptions.list`, `projects/subscriptions.modifyAckDeadline`, `projects/subscriptions.modifyPushConfig`, `projects/subscriptions.patch`, `projects/subscriptions.seek`, `projects/subscriptions.setIamPolicy`, `projects/subscriptions.testIamPermissions`, `projects/topics.delete`, `projects/topics.get`, `projects/topics.getIamPolicy`, `projects/topics.patch`, `projects/topics.publish`, `projects/topics.testIamPermissions`, `projects/topics/snapshots.list`

### reseller v1 (4 not called)

`customers.update`, `resellernotify.getwatchdetails`, `resellernotify.register`, `resellernotify.unregister`

### searchconsole v1 (10 not called)

`searchanalytics.query`, `sitemaps.delete`, `sitemaps.get`, `sitemaps.list`, `sitemaps.submit`, `sites.add`, `sites.delete`, `sites.get`, `urlInspection/index.inspect`, `urlTestingTools/mobileFriendlyTest.run`

### servicemanagement v1 (21 not called)

`operations.list`, `services.create`, `services.delete`, `services.generateConfigReport`, `services.get`, `services.getConfig`, `services.getIamPolicy`, `services.list`, `services.setIamPolicy`, `services.testIamPermissions`, `services.undelete`, `services/configs.create`, `services/configs.get`, `services/configs.list`, `services/configs.submit`, `services/consumers.getIamPolicy`, `services/consumers.setIamPolicy`, `services/consumers.testIamPermissions`, `services/rollouts.create`, `services/rollouts.get`, `services/rollouts.list`

### serviceusage v1 (7 not called)

`operations.cancel`, `operations.delete`, `operations.list`, `services.batchEnable`, `services.batchGet`, `services.disable`, `services.get`

### sheets v4 (10 not called)

`spreadsheets.getByDataFilter`, `spreadsheets/developerMetadata.get`, `spreadsheets/developerMetadata.search`, `spreadsheets/sheets.copyTo`, `spreadsheets/values.batchClearByDataFilter`, `spreadsheets/values.batchGetByDataFilter`, `spreadsheets/values.batchUpdateByDataFilter`, `spreadsheets/values.clear`, `spreadsheets/values.get`, `spreadsheets/values.update`

### siteVerification v1 (4 not called)

`webResource.delete`, `webResource.get`, `webResource.patch`, `webResource.update`

### storage v1 (82 not called)

`anywhereCaches.disable`, `anywhereCaches.get`, `anywhereCaches.insert`, `anywhereCaches.list`, `anywhereCaches.resume`, `anywhereCaches.update`, `bucketAccessControls.delete`, `bucketAccessControls.get`, `bucketAccessControls.insert`, `bucketAccessControls.list`, `bucketAccessControls.patch`, `bucketAccessControls.update`, `buckets.delete`, `buckets.get`, `buckets.getIamPolicy`, `buckets.getStorageLayout`, `buckets.insert`, `buckets.list`, `buckets.lockRetentionPolicy`, `buckets.patch`, `buckets.relocate`, `buckets.restore`, `buckets.setIamPolicy`, `buckets.testIamPermissions`, `buckets.update`, `defaultObjectAccessControls.delete`, `defaultObjectAccessControls.get`, `defaultObjectAccessControls.insert`, `defaultObjectAccessControls.list`, `defaultObjectAccessControls.patch`, `defaultObjectAccessControls.update`, `folders.delete`, `folders.deleteRecursive`, `folders.get`, `folders.insert`, `folders.list`, `folders.rename`, `managedFolders.delete`, `managedFolders.get`, `managedFolders.getIamPolicy`, `managedFolders.insert`, `managedFolders.list`, `managedFolders.setIamPolicy`, `managedFolders.testIamPermissions`, `managedFolders.update`, `notifications.delete`, `notifications.get`, `notifications.insert`, `notifications.list`, `objectAccessControls.delete`, `objectAccessControls.get`, `objectAccessControls.insert`, `objectAccessControls.list`, `objectAccessControls.patch`, `objectAccessControls.update`, `objects.bulkRestore`, `objects.compose`, `objects.copy`, `objects.delete`, `objects.getIamPolicy`, `objects.insert`, `objects.move`, `objects.patch`, `objects.restore`, `objects.setIamPolicy`, `objects.testIamPermissions`, `objects.update`, `objects.viewFullContext`, `operations.advanceRelocateBucket`, `operations.cancel`, `operations.list`, `projects/hmacKeys.create`, `projects/hmacKeys.delete`, `projects/hmacKeys.get`, `projects/hmacKeys.list`, `projects/hmacKeys.update`, `projects/serviceAccount.get`, `rapidCaches.disable`, `rapidCaches.get`, `rapidCaches.insert`, `rapidCaches.list`, `rapidCaches.update`

### tagmanager v2 (105 not called)

`accounts.get`, `accounts.list`, `accounts.update`, `accounts/containers.combine`, `accounts/containers.create`, `accounts/containers.delete`, `accounts/containers.get`, `accounts/containers.list`, `accounts/containers.lookup`, `accounts/containers.move_tag_id`, `accounts/containers.snippet`, `accounts/containers.update`, `accounts/containers/destinations.get`, `accounts/containers/destinations.link`, `accounts/containers/destinations.list`, `accounts/containers/environments.create`, `accounts/containers/environments.delete`, `accounts/containers/environments.get`, `accounts/containers/environments.list`, `accounts/containers/environments.reauthorize`, `accounts/containers/environments.update`, `accounts/containers/version_headers.latest`, `accounts/containers/version_headers.list`, `accounts/containers/versions.delete`, `accounts/containers/versions.get`, `accounts/containers/versions.live`, `accounts/containers/versions.publish`, `accounts/containers/versions.set_latest`, `accounts/containers/versions.undelete`, `accounts/containers/versions.update`, `accounts/containers/workspaces.bulk_update`, `accounts/containers/workspaces.create`, `accounts/containers/workspaces.create_version`, `accounts/containers/workspaces.delete`, `accounts/containers/workspaces.get`, `accounts/containers/workspaces.getStatus`, `accounts/containers/workspaces.list`, `accounts/containers/workspaces.quick_preview`, `accounts/containers/workspaces.resolve_conflict`, `accounts/containers/workspaces.sync`, `accounts/containers/workspaces.update`, `accounts/containers/workspaces/built_in_variables.create`, `accounts/containers/workspaces/built_in_variables.delete`, `accounts/containers/workspaces/built_in_variables.list`, `accounts/containers/workspaces/built_in_variables.revert`, `accounts/containers/workspaces/clients.create`, `accounts/containers/workspaces/clients.delete`, `accounts/containers/workspaces/clients.get`, `accounts/containers/workspaces/clients.list`, `accounts/containers/workspaces/clients.revert`, `accounts/containers/workspaces/clients.update`, `accounts/containers/workspaces/folders.delete`, `accounts/containers/workspaces/folders.entities`, `accounts/containers/workspaces/folders.get`, `accounts/containers/workspaces/folders.list`, `accounts/containers/workspaces/folders.move_entities_to_folder`, `accounts/containers/workspaces/folders.revert`, `accounts/containers/workspaces/folders.update`, `accounts/containers/workspaces/gtag_config.create`, `accounts/containers/workspaces/gtag_config.delete`, `accounts/containers/workspaces/gtag_config.get`, `accounts/containers/workspaces/gtag_config.list`, `accounts/containers/workspaces/gtag_config.update`, `accounts/containers/workspaces/tags.create`, `accounts/containers/workspaces/tags.delete`, `accounts/containers/workspaces/tags.get`, `accounts/containers/workspaces/tags.list`, `accounts/containers/workspaces/tags.revert`, `accounts/containers/workspaces/tags.update`, `accounts/containers/workspaces/templates.create`, `accounts/containers/workspaces/templates.delete`, `accounts/containers/workspaces/templates.get`, `accounts/containers/workspaces/templates.import_from_gallery`, `accounts/containers/workspaces/templates.list`, `accounts/containers/workspaces/templates.revert`, `accounts/containers/workspaces/templates.update`, `accounts/containers/workspaces/transformations.create`, `accounts/containers/workspaces/transformations.delete`, `accounts/containers/workspaces/transformations.get`, `accounts/containers/workspaces/transformations.list`, `accounts/containers/workspaces/transformations.revert`, `accounts/containers/workspaces/transformations.update`, `accounts/containers/workspaces/triggers.create`, `accounts/containers/workspaces/triggers.delete`, `accounts/containers/workspaces/triggers.get`, `accounts/containers/workspaces/triggers.list`, `accounts/containers/workspaces/triggers.revert`, `accounts/containers/workspaces/triggers.update`, `accounts/containers/workspaces/variables.create`, `accounts/containers/workspaces/variables.delete`, `accounts/containers/workspaces/variables.get`, `accounts/containers/workspaces/variables.list`, `accounts/containers/workspaces/variables.revert`, `accounts/containers/workspaces/variables.update`, `accounts/containers/workspaces/zones.create`, `accounts/containers/workspaces/zones.delete`, `accounts/containers/workspaces/zones.get`, `accounts/containers/workspaces/zones.list`, `accounts/containers/workspaces/zones.revert`, `accounts/containers/workspaces/zones.update`, `accounts/user_permissions.create`, `accounts/user_permissions.delete`, `accounts/user_permissions.get`, `accounts/user_permissions.list`, `accounts/user_permissions.update`

### tasks v1 (2 not called)

`tasklists.update`, `tasks.update`

### vault v1 (10 not called)

`matters.close`, `matters.delete`, `matters.reopen`, `matters.undelete`, `matters/holds.addHeldAccounts`, `matters/holds.removeHeldAccounts`, `matters/holds/accounts.list`, `operations.cancel`, `operations.delete`, `operations.list`

### youtube v3 (81 not called)

`abuseReports.insert`, `activities.list`, `captions.delete`, `captions.download`, `captions.insert`, `captions.list`, `captions.update`, `channelBanners.insert`, `channelSections.delete`, `channelSections.insert`, `channelSections.list`, `channelSections.update`, `channels.update`, `commentThreads.insert`, `commentThreads.list`, `comments.delete`, `comments.insert`, `comments.markAsSpam`, `comments.setModerationStatus`, `comments.update`, `i18nLanguages.list`, `i18nRegions.list`, `liveBroadcasts.bind`, `liveBroadcasts.delete`, `liveBroadcasts.insert`, `liveBroadcasts.insertCuepoint`, `liveBroadcasts.list`, `liveBroadcasts.transition`, `liveBroadcasts.update`, `liveChatBans.delete`, `liveChatBans.insert`, `liveChatMessages.delete`, `liveChatMessages.insert`, `liveChatMessages.list`, `liveChatMessages.transition`, `liveChatModerators.delete`, `liveChatModerators.insert`, `liveChatModerators.list`, `liveStreams.delete`, `liveStreams.insert`, `liveStreams.list`, `liveStreams.update`, `members.list`, `membershipsLevels.list`, `playlistImages.delete`, `playlistImages.insert`, `playlistImages.list`, `playlistImages.update`, `playlistItems.delete`, `playlistItems.insert`, `playlistItems.list`, `playlistItems.update`, `playlists.delete`, `playlists.insert`, `playlists.list`, `playlists.update`, `search.list`, `subscriptions.delete`, `subscriptions.insert`, `subscriptions.list`, `superChatEvents.list`, `tests.insert`, `thirdPartyLinks.delete`, `thirdPartyLinks.insert`, `thirdPartyLinks.list`, `thirdPartyLinks.update`, `thumbnails.set`, `videoAbuseReportReasons.list`, `videoCategories.list`, `videoTrainability.get`, `videos.batchGetStats`, `videos.delete`, `videos.getRating`, `videos.insert`, `videos.list`, `videos.rate`, `videos.reportAbuse`, `videos.update`, `watermarks.set`, `watermarks.unset`, `youtube/v3/liveChat/messages.stream`

